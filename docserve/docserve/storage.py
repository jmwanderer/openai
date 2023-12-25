import datetime
import logging
import os
import sqlite3



def data_path(app):
  return os.path.join(app.instance_path, 'data')

def add_user_doc(db, user_id, doc_id, filename):
  logging.info(f"add user doc: {user_id}:{doc_id}") 
  db.execute("INSERT INTO documents (user_id, doc_id, filename) " +
             "VALUES (?,?, ?)", (user_id, doc_id, filename))
  db.commit()


def gen_filename():
  base_name = os.urandom(8).hex()  
  return f'{base_name}.ddf'
  
def get_doc_filename(db, user_id, doc_id):
  filename = None
  q = db.execute("SELECT filename FROM documents WHERE user_id = ? " +
                 "AND doc_id = ?", (user_id,doc_id))
  result = q.fetchone()
  if result is not None:
    filename = result[0]
  return filename

def get_user_doc_ids(db, user_id):
  result = []
  q = db.execute("SELECT doc_id FROM documents WHERE user_id = ?", (user_id,))
  for (doc_id,) in q.fetchall():
    result.append(doc_id)
  return result

def check_user_id(db, user_id):
  logging.info("check user_id: %s", user_id)
  q = db.execute("SELECT COUNT(*) from users WHERE user_id = ?", (user_id,))
  result = q.fetchone()[0] > 0
  logging.info("user_id result: %s", result)
  return result
  
def get_user_id(db, gpt_convo_id, gpt_user_id):
  logging.info(f"get_user_id for {gpt_convo_id}/{gpt_user_id}")

  # 4 Cases to handle:
  # 1 (default): existing user id entry for gpt values
  # 2: new gpt user, new gpt convo  
  # 3: existing gpt user, new convo
  # 4: existing convo with new gpt user (may exist, not with this convo


  # Case 1
  logging.info("case 1")
  q = db.execute("SELECT user_id FROM convo_users WHERE gpt_convo_id = ? " +
                 "AND gpt_user_id = ?", (gpt_convo_id, gpt_user_id))
  result = q.fetchone()
  if result is not None:
    user_id = result[0]
    note_user_entry(db, user_id)
    return user_id
  logging.info("no entry for convo_id and gpt_user_id")

  # Lookup entries for convo and user
  q = db.execute("SELECT user_id FROM convo_users WHERE gpt_convo_id = ?",
                 (gpt_convo_id,))
  result = q.fetchone()
  convo_user_id = None
  if result is not None:
    convo_user_id = result[0]

  q = db.execute("SELECT user_id FROM convo_users WHERE gpt_user_id = ?",
                 (gpt_user_id,))
  result = q.fetchone()
  gptuser_user_id = None
  if result is not None:
    gptuser_user_id = result[0]

  # Case 2: new gpt user, new gpt convo
  logging.info("case 2")  
  if convo_user_id is None and gptuser_user_id is None:
    user_id = os.urandom(8).hex()
    logging.info("new convo_id and new gpt_user_id")
    logging.info("create new user and entry: %s", user_id)
    add_user_entry(db, user_id)
    add_convo_entry(db, gpt_convo_id, gpt_user_id, user_id)
    return user_id

  # Case 3: new convo, existing user
  logging.info("case 3")    
  if convo_user_id is None and gptuser_user_id is not None:
    logging.info("new convo_id, existing gpt_user_id")
    user_id = gptuser_user_id
    note_user_entry(db, user_id)      
    add_convo_entry(db, gpt_convo_id, gpt_user_id, user_id)
    return user_id

  # 4: existing convo, but either new user or user doesn't match
  logging.info("case 4")        
  logging.info("existing convo, new or not matching gpt user")
  user_id = convo_user_id
  note_user_entry(db, user_id)      
  
  # Need to:
  # 2. update this convo entry to have the new gpt user
  # 2. update user_id for any entries created by new user
  #    connect any docs created by this user

  # Associate this convo with the new GPT user ID
  db.execute("UPDATE convo_users SET gpt_user_id = ? WHERE gpt_convo_id = ?",
             (gpt_user_id, gpt_convo_id))
  
  # Connect to any docs already created by the new user
  db.execute("UPDATE convo_users SET user_id = ? WHERE user_id = ?",
             (user_id, gptuser_user_id))
  db.execute("UPDATE documents SET user_id = ? WHERE user_id = ?",
             (user_id, gptuser_user_id))
  db.commit()

  logging.info("Change GPTUser for convo %s to %s", gpt_convo_id, gpt_user_id)
  logging.info("Change user_id %s to user_id %s in all docs and convos",
               gptuser_user_id, user_id)
  return user_id

def xfer_user_id(db, old_user_id, new_user_id):
  # Replace old_user_id with new_user_id
  # Give all docs to new user
  db.execute("UPDATE convo_users SET user_id = ? WHERE user_id = ?",
             (new_user_id, old_user_id))
  db.execute("UPDATE documents SET user_id = ? WHERE user_id = ?",
             (new_user_id, old_user_id))
  db.commit()


  
def add_convo_entry(db, gpt_convo_id, gpt_user_id, user_id):
  logging.info("add convo entry: %s/%s/%s", gpt_convo_id,
               gpt_user_id, user_id)
  
  db.execute("INSERT INTO convo_users (gpt_convo_id, gpt_user_id, user_id) " +
             "VALUES (?,?,?)",
             (gpt_convo_id, gpt_user_id, user_id))
  db.commit()  

def dump_tables(db):
  q = db.execute("SELECT user_id, created, last_access FROM users")
  print("users table:")
  for (user_id, created, last_access) in q.fetchall():
    created_dt = datetime.datetime.fromtimestamp(created)        
    access_dt = datetime.datetime.fromtimestamp(last_access)
    print("%s\t created=%s\t last access=%s" % (user_id,
                                                created_dt.isoformat(sep=' '),
                                                access_dt.isoformat(sep=' ')))

  print("")
  q = db.execute("SELECT gpt_convo_id, gpt_user_id, user_id FROM convo_users")
  print("convo_user table:")
  for (convo_id, gpt_user_id, user_id) in q.fetchall():
    print(f"\t{convo_id}\t{gpt_user_id}\t{user_id}")
  print("")

  q = db.execute("SELECT user_id, doc_id, filename FROM documents")
  print("documents table:")
  for (user_id, doc_id, filename) in q.fetchall():
    print(f"\t{user_id}\t{doc_id}\t{filename}")
  print("")
  
  q = db.execute("SELECT address, start_time, last_update, count FROM access")
  print("access table:")
  for (address, start_time, last_update, count) in q.fetchall():
    start_time = datetime.datetime.fromtimestamp(start_time).isoformat()
    last_update = datetime.datetime.fromtimestamp(last_update).isoformat()
    print(f"\t{address}\t{start_time}\t{last_update}\t{count}")
    
  
def note_user_entry(db, user_id):
  # update access time
  now = datetime.datetime.now()  
  db.execute("UPDATE users SET last_access = ? WHERE user_id = ?",
             (now.timestamp(), user_id))
  db.commit()

def add_user_entry(db, user_id):
  now = datetime.datetime.now()  
  db.execute("INSERT INTO users (user_id, created, last_access) " +
             "VALUES (?,?,?)",
             (user_id, now.timestamp(), now.timestamp()))
  db.commit()  
  
             
def check_address_block(db, address):
  now = datetime.datetime.now()
  hour_past = now.timestamp() - (60 * 5)
  q = db.execute("SELECT start_time, last_update, count FROM access " +
                 "WHERE address = ? and last_update > ?",
                 (address, hour_past))
  result = q.fetchone()
  if result is not None:
    (start_time, last_update, count) = result
    time_delta = last_update - start_time
    if time_delta > 0 and count > 10:
      ratio = count / (last_update - start_time)
      if ratio > 0.1:
        logging.info("address %s blocked with ratio %f", address, ratio)
        return True
  return False


def inc_bad_access(db, address):
  logging.info("Inc bad access %s", address)
  now = datetime.datetime.now()
  # Cleanup any old records
  hour_past = now.timestamp() - (60 * 5)
  db.execute("DELETE FROM access WHERE last_update < ?", (hour_past,))

  # Insert or update for this address
  q = db.execute("SELECT count FROM access WHERE address = ?", (address,))
  result = q.fetchone()
  if result is not None:
    (count,) = result
    db.execute("UPDATE access SET count = ?, last_update = ? " +
               "WHERE address = ?", (count + 1, now.timestamp(), address))
  else:
    db.execute("INSERT INTO access (address, start_time, last_update, count) " +
               "VALUES (?, ?, ?, ?)", (address, now.timestamp(),
                                       now.timestamp(), 1))
  db.commit()
    

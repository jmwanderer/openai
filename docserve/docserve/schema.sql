DROP TABLE IF EXISTS convo_users;
DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS users;

CREATE TABLE convo_users (
  gpt_convo_id TEXT UNIQUE NOT NULL,
  gpt_user_id TEXT NOT NULL,
  user_id TEXT NOT NULL
);

CREATE TABLE documents (
  doc_id TEXT UNIQUE NOT NULL,
  user_id TEXT NOT NULL,
  filename TEXT NOT NULL,
  UNIQUE(doc_id, user_id)
);      

CREATE TABLE users (
  user_id TEXT UNIQUE NOT NULL,
  created INTEGER DEFAULT 0,
  last_access INTEGER DEFAULT 0
);


CREATE TABLE access (
  address TEXT UNIQUE NOT NULL,
  start_time INTEGER DEFAULT 0,
  last_update INTEGER DEFAULT 0,
  count INTEGER DEFAULT 0
);

  

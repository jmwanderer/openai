# DocServe / Article Assistant

DocServe is a backend for a custom OpenAI GPT, Article Assistant.
Article Assitant is an experiment in using GPT Actions to enable
ChatGPT to build a document a piece at a time. DocServer is a flask based
server supporting the actions that allow ChatGPT to build a document.

The DocServer project cointains everything requires to configure a
custom GPT and run the server.

# Install and Configure DocServe

Ensure you are using Python 3.6 and later.
```
git clone https://github.com/jmwanderer/openai
cd openai
python3 -m venv venv
. venv/bin/activate
cd docserve
pip install -r docserve/requirements.txt
```

## Configuration

### Create an SQLite Database
```
cd openai/docserve
flask --app docserver.server init-db
```

### Generate a secret API Auth Key

```
python3 -c "import os; print(os.urandom(10).hex())"
```

### Configure secret API Key

Set in the config.py file:

```
cd openai/docserve
echo 'AUTH="secret-key" > instance/config.py'
```

or in the environment:

```
export FLASK_AUTH="secret-key"
```

# Run a Debug Server

```
cd openai
. venv/bin/activate
cd docserve
flask --app docserver.server init-db
```

# Run a Production Server

Good choices for a production service include waitress and Gunicorn.

```
cd openai
. venv/bin/activate
cd docserve
waitress --app docserver.server init-db
```

# Build a custom GPT

ChatGTP -> My GPT -> Create a GPT

- Set instructions from docserve/instructions/txt
- Customize servers in docserve/openapi.json.
'''
"url": "https://www.example.com"
'''
- Configure actions with openapi.json - copy and paste


# Build a PIP package

```
cd openai
. venv/bin/activate
cd docserve
make build
```







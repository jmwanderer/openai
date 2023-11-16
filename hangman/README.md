# Hangman Game

A simple implementation of the letter guessing game hangman.

This module supports:
- Running a basic hangman game in a terminal.
- Running a game in the terminal using the ChatGPT API.
- Running a flask server to provide a hangman HTTP API.

## Run Tests:

`python3 -m unittest hangman/hangman_test.py`


## Play a game in the terminal:

`python3 -m hangman.hangman  [ WORD_SIZE  NUM_GUESSES ]`

## Play a game with the ChatGPT LLM:

`export OPENAI_API_KEY=<key>`

`python3 -m hangman.chat`

## Run the Hangman API server
(Debug mode)

`flask --app hangman.server run --debug`

For a deployment that can be accessed from the internet, use
a production server (e.g. waitress) and consider a front end
proxy (e.g. Apache or Nginx)

# Hangman Game

A simple implementation of the letter guessing game hangman.

Test:

python3 -m unittest hangman/hangman_test.py


Play a game in the terminal:

python3 -m hangman.hangman  [ WORD_SIZE  NUM_GUESSES ]

Play a game with the ChatGPT LLM:

export OPENAI_API_KEY=<key>

python3 -m hangman.chat




Run the app in debug mode with:

`flask --app hangman.server run --debug`

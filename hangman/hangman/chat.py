#!/usr/bin/env python3
"""
Text chat client that can make function calls to hangman.

From: https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models
"""

import os
import json
import openai
import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored

from . import hangman

GPT_MODEL = "gpt-3.5-turbo-0613"
openai.api_key = os.environ['OPENAI_API_KEY']

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, functions=None, function_call=None, model=GPT_MODEL):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages}
    if functions is not None:
        json_data.update({"functions": functions})
    if function_call is not None:
        json_data.update({"function_call": function_call})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
            timeout=10,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

  
def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "white",
        "assistant": "green",
        "function": "magenta",
    }
    
    for message in messages:
        if message["role"] == "system":
            print(colored(f"system: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "user":
            print(colored(f"user: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and message.get("function_call"):
            print(colored(f"assistant: {message['function_call']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and not message.get("function_call"):
            print(colored(f"assistant: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "function":
            print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))

def print_assistant(message):
  print(colored(f"{message['content']}\n", "green"))
  

functions = [
    {
        "name": "start_new_hangman_game",
        "description": "Start a new game",
        "parameters": {
            "type": "object",
            "properties": {
                "word_size": {
                    "type": "integer",
                    "description": "Size of word to guess",
                },
                "max_wrong_guesses": {
                    "type": "integer",
                    "description": "The number of wrong guesses allowed.",
                },
            },
            "required": ["word_size", "max_wrong_guesses"],
        },
        "returns": {
          "type": "string",
          "description": "The word to guess",
        },
    },
    {
        "name": "record_guess",
        "description": "Record a guess made by the player.",
        "parameters": {
            "type": "object",
            "properties": {
                "letter": {
                    "type": "string",
                    "description": "The letter guessed by the player.",
                },
            },
            "required": ["letter"]
        },
        "returns": {
          "type": "object",
          "properties": {
            "found" : {
              "type": "boolean",
              "description": "Was the letter found in the word",
            },
            "visible_word" : {
              "type": "string",
              "description": "The current view of the word.",
            },
            "word" : {
              "type": "string",
              "description": "The secret word.",
            },
            "remaining_guesses" : {
              "type": "integer",
              "description": "The number of remaining guesses for the player",
            },
            "status" : {
              "type": "string",
              "enum": ["won", "lost", "inprogress"], 
              "description": "Current sate of the game",
            },
          },
        },
    },
]            




def execute_function_call(function_call):
  if function_call["name"] == "start_new_hangman_game":
    arguments = json.loads(function_call['arguments'])
    game.new_game(int(arguments['word_size']), int(arguments['max_wrong_guesses']))
    return game.word

  if function_call["name"] == "record_guess":
    arguments = json.loads(function_call['arguments'])    
    result = game.guess_letter(arguments['letter'])

    game_state = game.get_game_state()

    if game_state.status == hangman.GAME_WON:
      status = "won"
    elif game_state.status == hangman.GAME_LOST:
      status = "lost"
    else:
      status = "inprogress"
  
    content = { "found" : result,
                "visible_word" : game_state.word,
                "word" : game.word,                
                "remaining_guesses" : game.guesses_remaining,
                "status" : status }
    return json.dumps(content)

  return ""


messages = []
messages.append({"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
messages.append({"role": "user", "content": "Lets play hangman"})
pretty_print_conversation([messages[1]])

chat_response = chat_completion_request(
    messages, functions=functions
)
assistant_message = chat_response.json()["choices"][0]["message"]
messages.append(assistant_message)

game = hangman.Game()
while True:
  # Process function calls
  if assistant_message.get("function_call"):
    content = execute_function_call(assistant_message["function_call"])
    messages.append({"role": "function", "name": assistant_message["function_call"]["name"],
                     "content": content})
  else:
    print_assistant(assistant_message)
    user = input("> ").strip()
    if user == 'exit':
      break
    messages.append({"role": "user", "content": user})

  chat_response = chat_completion_request(
    messages, functions=functions
  )
  assistant_message = chat_response.json()["choices"][0]["message"]
  messages.append(assistant_message)


pretty_print_conversation(messages)
  




#!/usr/bin/env python3
"""
Core logic for the game hangman.
"""
import random
import sys

# Enumeration for current game state.
GAME_WON=1
GAME_LOST=2
GAME_IN_PROGRESS=3

class Game:
    def __init__(self):
        self.word = None
        self.guesses = None
        self.guesses_remaining = 0

    def new_game(self, word_len, allowed_wrong_guesses):
        """
        Set state to start a new game with max_guesses allowed.
        Select a new word matching the given length.
        """
        word_len = max(word_len, 2)
        word_len = min(word_len, 21)        
        self.word = self.get_random_word(word_len)
        self.guesses = []
        self.guesses_remaining = allowed_wrong_guesses

    def guess_letter(self, letter):
        """
        Record a guess and return true if guessed letter is in the word
        """
        letter = letter.lower()
        if self.guesses_remaining > 0 and not letter in self.guesses:
            self.guesses.append(letter)
        if letter in self.word:
            return True
        else:
            self.guesses_remaining -= 1
            return False

    def get_game_state(self):
        """
        Return the current state of the game.
        """
        game_state = GameState()
        game_won = True
        for letter in self.word:
            if letter in self.guesses:
                game_state.word += letter + ' '
            else:
                game_state.word += '_ '
                game_won = False
        game_state.word = game_state.word.strip()

        if game_won:
            game_state.status = GAME_WON
        elif self.guesses_remaining < 1:
            game_state.status = GAME_LOST
        else:
            game_state.status = GAME_IN_PROGRESS
        return game_state
            
    def build_word_list(self, word_length):
        candidates = []
        f = open("/usr/share/dict/words", "r")
        for word in f.readlines():
            word = word.strip()
            if (len(word) == word_length and
                not "'" in word and
                not word[0].isupper() and
                not word[-1] == 's' and
                not word[-2:] == 'ed'):                
                candidates.append(word)
        f.close()
        return candidates

    def get_random_word(self, word_length):
        candidates = self.build_word_list(word_length)
        return candidates[random.randint(0, len(candidates) - 1)]

    def play_test_game(self):
        guesses = "abcdefghijklmnopqrstuvwxyz"
        print("word: %s" % self.word)
        while self.get_game_state().status == GAME_IN_PROGRESS:
            index = random.randint(0, len(guesses) - 1)
            letter = guesses[index]
            guesses = guesses[:index] + guesses[index+1:]
            result = self.guess_letter(letter)
            print("guess %s - %s" % (letter, result))
            print(self.get_game_state().to_string())


class GameState:
    def __init__(self):
        self.word = ""
        self.status = 0

    def to_string(self):
        result = "Word: " + self.word + '\n'
        result += "Game: "
        if self.status == GAME_WON:
            result += "WIN!"
        elif self.status == GAME_LOST:
            result += "Loss"
        else:
            result += "In Progress"
        return result


def play(word_len, num_guesses):
    game = Game()
    game.new_game(word_len, num_guesses)

    while game.get_game_state().status == GAME_IN_PROGRESS:
        print()
        print(game.get_game_state().to_string())
        print("guesses: %s" % " ".join(game.guesses))
        guess = input("enter guess: ").strip()
        if len(guess) > 0:
            letter = guess[0]
            result = game.guess_letter(letter)
            print("guess %s - %s" % (letter, result))
    print()
    print(game.get_game_state().to_string())            
    print("word: %s" % game.word)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        play(int(sys.argv[1]), int(sys.argv[2]))
    else:
        play(6, 15)
    
        
    
        
        

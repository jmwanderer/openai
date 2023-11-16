#!/usr/bin/env python3
from . import hangman
import unittest

class GameTestCase(unittest.TestCase):
  def setUp(self):
    self.game = hangman.Game()

  def testSimpleWin(self):
    self.game.new_game(6, 12)
    self.game.word = 'cowboy'    
    print(self.game.get_game_state().to_string())
    guesses = "acnymvboxw"
    for letter in guesses:
      result = self.game.guess_letter(letter)
      print("guess %s - %s" % (letter, result))
      print(self.game.get_game_state().to_string())
    self.assertEqual(self.game.get_game_state().status, hangman.GAME_WON)

  def testSimpleLoss(self):
    self.game.new_game(6, 8)
    self.game.word = 'cowboy'    
    print(self.game.get_game_state().to_string())
    guesses = "acnymvbxwkjgdf"
    for letter in guesses:
      result = self.game.guess_letter(letter)
      print("guess %s - %s" % (letter, result))
      print(self.game.get_game_state().to_string())
    self.assertEqual(self.game.get_game_state().status, hangman.GAME_LOST)

  def testPlaySmall(self):
    self.game.new_game(3, 15)
    self.assertEqual(len(self.game.word), 3)    
    self.game.play_test_game()
    
  def testPlayMedium(self):
    self.game.new_game(7, 15)
    self.assertEqual(len(self.game.word), 7)    
    self.game.play_test_game()
    
  def testPlayBig(self):
    self.game.new_game(10, 18)
    self.assertEqual(len(self.game.word), 10)
    self.game.play_test_game()

  def testPlayBigWin(self):
    self.game.new_game(10, 26)
    self.assertEqual(len(self.game.word), 10)
    self.game.play_test_game()
    self.assertEqual(self.game.get_game_state().status, hangman.GAME_WON)
    



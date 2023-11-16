from genthought import WriteThought
import os.path
import os
import unittest
from unittest.mock import patch
import tempfile


class GenThoughtTestCase(unittest.TestCase):

  testdir = tempfile.gettempdir()
  testfile = os.path.join(testdir, 'thought.html')

  @patch('genthought.openai.ChatCompletion')
  def testGenThought(self, mock_chat):
    mock_chat.create.return_value = { 'choices' :
                                      [ { 'message' :
                                          { 'content' : "short reply"}}]}

    if os.path.isfile(self.testfile):
      os.remove(self.testfile)
    WriteThought(self.testdir)
    self.assertTrue(os.path.isfile(self.testfile), "Gen file failed.")

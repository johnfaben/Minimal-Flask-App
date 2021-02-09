from replit import db
import random

class Answer():
  pass

class Hipe():
  def __init__(self,letters):
    if letters in db:
       self.letters = letters
       self.answers = db[self.letters]
    else:
      self.letters = None
      
def random_hipe():
  letters = random.choice([letters for letters in db])
  return Hipe(letters)
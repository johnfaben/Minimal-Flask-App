from replit import db
import random

class Answer():
  pass

class Hipe():
  def __init__(self,letters):
    if letters in db:
       self.letters = letters
       self.answers = db[self.letters][1:]
       self.votes = db[self.letters][0]
    else:
      self.letters = None
      
  def add_vote(self):
    db[self.letters][0] = self.votes +1 
      
def random_hipe():
  letters = random.choice([letters for letters in db])
  return Hipe(letters)

def delete_hipe(letters):
  del db[letters]


from replit import db
from flask_login import UserMixin
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
      
  def add_like(self):
    db[self.letters] = [db[self.letters][0] +1] + db[self.letters][1:]
    self.votes = db[self.letters][0] 
      
def random_hipe():
  letters = random.choice([letters for letters in db])
  return Hipe(letters)

def delete_hipe(letters):
  del db[letters]

class User(UserMixin):
    def __init__(self, id_, name, email):
        self.id = id_
        self.name = name
        self.email = email

    @staticmethod
    def get(user_id):
        user = 0
        if user_id in db:
          user = User(id_ = user_id, name = db[user_id][0],email=db[user_id][1])
        if not user:
            return None
        return user

    @staticmethod
    def create(id_, name, email):
        db[id_] = [name,email]
    
    def add_hipe_to_liked(self,letters):
        if letters not in db[self.id]:
          db[self.id] = db[self.id] + [letters]
          return True
        return False
    
    def get_liked(self):
      if len(db[self.id]) > 2:
        return db[self.id][2:]
      return []
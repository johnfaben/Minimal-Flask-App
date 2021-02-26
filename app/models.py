from flask_login import UserMixin
import os
import pymongo
import datetime

client = pymongo.MongoClient(os.environ.get('MONGO_DB_STRING'))
database = client.hipegame

class Answer():
  pass

class Hipe():
  def __init__(self,letters):
    db_result = list(database.hipes.find({'letters':letters}))
    if db_result:
       self.letters = db_result[0]['letters']
       self.answers = db_result[0]['answers']
       
    else:
      self.letters = None
      
  def get_votes(self):
    return len(list(database.likes.find({'letters':self.letters})))
      
def random_hipe():
  letters = database.hipes.aggregate([{'$sample':{'size':1}}]).next()['letters']
  return Hipe(letters)

def delete_hipe(letters):
  database.hipes.delete_one({'letters':letters})

class User(UserMixin):
    def __init__(self, id_, name, email):
        self.id = id_
        self.name = name
        self.email = email

    @staticmethod
    def get(user_id):
        user = 0
        if len(list(database.users.find({'user_id':user_id}))) > 0:
          user_dict = list(database.users.find({'user_id':user_id}))[0]
          user = User(id_ = user_id, name = user_dict['user_name'],email= user_dict['user_email'])
        if not user:
            return None
        return user

    @staticmethod
    def create(id_, name, email):
        database.users.insert_one({'user_id':id_,'user_name':name,'user_email':email})

    def get_liked(self):
      return [like['letters'] for like in database.likes.find({'user_id': self.id})]


    def get_solved(self):

      return [solve['letters'] for solve in database.solved.find({'user_id': self.id})]


    def add_solve(self,hipe):
      answered = dict()
      answered['user_id'] = self.id
      answered['letters'] = hipe.letters
      answered['timestamp'] = datetime.datetime.now()
      database.solved.insert_one(answered)

    def add_like(self,hipe):
      if len(list(database.likes.find({'letters':hipe.letters},{'user_id':self.id}))) == 0:
        like = dict()
        like['user_id'] = self.id
        like['letters'] = hipe.letters
        like['timestamp'] = datetime.datetime.now()
        database.likes.insert_one(like)
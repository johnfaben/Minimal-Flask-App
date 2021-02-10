from replit import db
from time import sleep

def add_hipes():
  print('populating list of HIPEs from the file')
  db.clear()
  i = 0
  with open('list_of_hipes.txt','r') as f:
    for line in f:
      i+=1
      line = line.strip().split(',')
      letters = line[0]
      answers = line[1:]
      db[letters] = [0] + answers
      if i%100 == 0:
        sleep(5)
        print('loaded %d hipes, waiting 5 seconds to avoid spamming the database' %i)
        print(line)
  
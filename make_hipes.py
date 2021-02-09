from replit import db

def add_hipes():
  db.clear()
  f = open('list_of_hipes.txt','r')
  for i in range(10):
    line = f.readline()
    line = line.strip().split(',')
    letters = line[0]
    answers = line[1:]
    db[letters] = answers
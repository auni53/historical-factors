from db import Database
import pickle
import os

import pdb
stop = pdb.set_trace

WORDS = "socialism communism russia gem jewel capitalism fruit furnace".split(' ')

def get_monocount(db, word, year):
  query = '''
    SELECT SUM(count)
    FROM bigrams
    WHERE (w1 = %s
        or w2 = %s)
      and year = %d
  '''
  occurrences = db.execute(query, word, word, year)
  return list(occurrences)[0][0]

def get_monograms(year):
  path = 'data/jar/{}-monogram.p'.format(year)
  print "Getting monograms for %d" % year
  if os.path.exists(path):
    with open(path, 'r') as f:
      monograms = pickle.load(f)
  else:
    db = Database()
    monograms = {}
    print "Counting monograms for %d" % year
    for word in WORDS:
      count = get_monocount(db, word, year)
      monograms[word] = count
    db.close()

    with open(path, 'w') as f:
      pickle.dump(monograms, f)

  print "Got monograms for %d" % year
  return monograms

def get_bicount(db, word, year):
  query = '''
    SELECT w1, w2, count
    FROM bigrams
    WHERE (w1 = %s
        or w2 = %s)
      and year = %d
  '''
  occurrences = db.execute(query, word, word, year)
  return list(occurrences)

def get_bigrams(year):
  path = 'data/jar/{}-bigram.p'.format(year)
  print "Getting bigrams for %d" % year
  if os.path.exists(path):
    with open(path, 'r') as f:
      bigrams = pickle.load(f)
  else:
    db = Database()
    bigrams = {}
    print "Counting bigrams for %d" % year
    for word in WORDS:
      results = get_bicount(db, word, year)
      for row in results:
        w1 = row[0].encode('utf8').lower()
        w2 = row[1].encode('utf8').lower()
        c  = row[2]
        if word == w1:
          pair = (w1, w2,)
        elif word == w2:
          pair = (w2, w1,)
        if pair in bigrams:
          bigrams[pair] += c
        else:
          bigrams[pair] = c
    db.close()

    with open(path, 'w') as f:
      pickle.dump(bigrams, f)

  print "Got bigrams for %d" % year
  return bigrams


def ppmi(year):
  result = get_bigrams(year)

def main():
  for year in range(1880, 2010, 10):
    try:
      result = ppmi(year)
    except Exception as e:
      print "Had problems with %d" % year
      print e

if __name__ == '__main__':
  main()

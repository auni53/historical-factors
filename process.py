from ngram_labels import ngram_labels
from db import Database
from joblib import Parallel, delayed
import multiprocessing
import os
import pdb
stop = pdb.set_trace

from itertools import islice

DATA_PATH = 'data/'

def get_file_list():
  isSplit = lambda x: (len(x.split('.')) == 2
                and x.split('.')[1] == 'bin')
                # and len(x.split('.')[2]))
  pathify = lambda s: DATA_PATH + s
  files = os.listdir(DATA_PATH)
  files.sort()
  return map(pathify, filter(isSplit, files))

def process(path):
  try:
    db = Database()
    with open(path) as f:
      print "processing %s" % path

      for line in f:
        if isInteresting(line):
          db.insert(line_to_value(line))
    print "committing %s" % path
    db.close()

  except Exception as e:
    print "Had problems with label %s" % path
    print e

  print "succeeded with %s" % path

def isInteresting(l):
  terms = "socialism communism russia gem jewel capitalism fruit furnace"
  words = terms.split(' ')
  if len(l) > 210:
    return False

  for w in words:
    if w in l.lower():
      return True
  return False

def line_to_value(l):
  try:
    ngram, year, count, volumes = l.strip().split('\t')
    w1, w2 = ngram.split(' ')
    value = (count, w1, w2, year, w1, w2, year, count)
    # value = (w1, w2, year, count)
    return value
  except Exception as e:
    stop()

def main():
  import bad; files = bad.bad
  print bad
  exit(0)
  # files = get_file_list()
  # files = ["data/google-ac.bin"]
  cores = multiprocessing.cpu_count()
  Parallel(n_jobs=cores)(delayed(process)(x) for x in files)
  # for x in files: process(x)

if __name__ == '__main__':
  main()


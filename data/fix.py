from download import ngram_labels
import os

import pdb
stop = pdb.set_trace

DATA_PATH = "./"
def get_file_list():
  isSplit = lambda x: (len(x.split('.')) == 3
                and x.split('.')[1] == 'bin'
                and len(x.split('.')[2]))
  pathify = lambda s: s
  files = os.listdir(DATA_PATH)
  files.sort()
  return map(pathify, filter(isSplit, files))

exclude = '0 1 2 3 4 5 6 7 8 9 _ADJ_'.split(' ')
labels = [x for x in ngram_labels if x not in exclude]
files = get_file_list()
for label in labels:
  relevant = [f for f in files if label in f]
  c = 0
  while c < len(relevant):
    prior = relevant[c - 1]
    suspect = relevant[c]
    with open(suspect, 'r') as f:
      head = f.readline()
      rest = f.read()
    with open(prior, 'a') as f:
      f.write(head)
    with open(suspect, 'w') as f:
      f.write(rest)
    c += 1

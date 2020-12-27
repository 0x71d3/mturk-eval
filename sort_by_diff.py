import csv
import os
import sys
from operator import itemgetter

from_dir, to_dir = sys.argv[1:]

from_scores = []
with open(os.path.join(from_dir, 'emotion.csv'), newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        labels = []
        for label in row:
            if label:
                labels.append(int(label))
        score = sum(labels) / len(labels)
        from_scores.append(score)

to_scores = []
with open(os.path.join(to_dir, 'emotion.csv'), newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        labels = []
        for label in row:
            if label:
                labels.append(int(label))
        score = sum(labels) / len(labels)
        to_scores.append(score)

assert len(to_scores) == len(from_scores)

diff_scores = []
for from_score, to_score in zip(from_scores, to_scores):
    diff_score = to_score - from_score
    diff_scores.append(diff_score)

print(*sorted(enumerate(diff_scores), key=itemgetter(1)), sep='\n')

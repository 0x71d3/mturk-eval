import csv
import os
import sys

attrs = ['emotion', 'fluency', 'informativeness', 'relevance']

result_dir = sys.argv[1]

for attr in attrs:
    scores = []
    with open(os.path.join(result_dir, attr + '.csv'), newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            labels = []
            for label in row:
                if label:
                    labels.append(int(label))
            score = sum(labels) / len(labels)
            scores.append(score)

    print(attr, sum(scores) / len(scores), sep='\t')

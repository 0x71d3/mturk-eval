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

            num_labels = len(labels)
            sorted_labels = sorted(labels)

            median_idx = num_labels // 2

            score = sorted_labels[median_idx]
            if num_labels % 2 == 0:
                score = (score + sorted_labels[median_idx+1]) / 2                
            scores.append(score)

    print(attr, sum(scores) / len(scores), sep='\t')

import argparse
import csv
import glob
import os
import sys

attrs = ['emotion', 'fluency', 'informativeness', 'relevance']

parser = argparse.ArgumentParser()
parser.add_argument('result_dir')
parser.add_argument('--ignoring', action='store_true')
args = parser.parse_args()

labels = {}

with open(glob.glob(args.result_dir + 'Batch_*_batch_results.csv')[0], newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row_labels = {}
        for attr in attrs:
            row_key = 'Answer.' + attr
            if not row[row_key]:
                row_key += '.label'
            label = int(row[row_key][0]) if row[row_key] else None
            row_labels[attr] = label
        
        if args.ignoring and len(set(row_labels.values())) == 1:
            row_labels = {attr: None for attr in attrs}

        for attr in attrs:
            if attr not in labels:
                labels[attr] = []
            labels[attr].append(row_labels[attr])
    
for attr in attrs:
    with open(os.path.join(args.result_dir, attr + '.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        for i in range(0, len(labels[attr]), 3):
            writer.writerow(labels[attr][i:i+3])

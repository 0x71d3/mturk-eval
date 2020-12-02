import argparse
import csv
import glob
import os

attrs = ['emotion', 'fluency', 'informativeness', 'relevance']

parser = argparse.ArgumentParser()

parser.add_argument('result_dir')

parser.add_argument('--num_assignments', type=int, default=100)
parser.add_argument('--num_tasks', type=int, default=10)
parser.add_argument('--num_workers', type=int, default=7)

parser.add_argument('--ignoring', action='store_true')

args = parser.parse_args()

res_paths = glob.glob(f'{args.result_dir}/Batch_*_batch_results.csv')
assert len(attrs) == len(res_paths)

attr_labels = {attr: [] for attr in attrs}

for attr, res_path in zip(attrs, res_paths):
    with open(res_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            labels = []
            for i in range(args.num_assignments // args.num_tasks):
                try:
                    key = f'Answer.{attr}{i}'
                    if key not in row or not row[key]:
                        key += '.label'
                    label = int(row[key][0])
                except IndexError:
                    label = None
                labels.append(label)

            if args.ignoring and len(set(labels)) == 1:
                labels = [None] * 10
            attr_labels[attr] += labels
    
    arranged = []
    for i in range(args.num_tasks):
        for j in range(args.num_assignments // args.num_tasks):
            for k in range(args.num_workers):
                index = (
                    i * args.num_tasks * args.num_workers
                    + j
                    + k * args.num_assignments // args.num_tasks
                )
                arranged.append(attr_labels[attr][index])
    
    attr_labels[attr] = arranged

for attr in attrs:
    labels = attr_labels[attr]
    with open(os.path.join(args.result_dir, attr + '.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        for i in range(0, len(labels), args.num_workers):
            writer.writerow(labels[i:i+args.num_workers])

import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument('input_path')
parser.add_argument('--model_name', type=str, default='target')
parser.add_argument('--num_samples', type=int, default=100)
args = parser.parse_args()

rows = []
with open(args.input_path, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append([row['source'], row[args.model_name]])

l = len(rows)
n = args.num_samples
with open(args.model_name + '.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['utterance', 'response'])
    for i in range(0, l, (l - 1) // n + 1):
        writer.writerow(rows[i])

import csv
import os
import sys

attrs = ['emotion', 'fluency', 'informativeness', 'relevance']

input_dirs = sys.argv[1:-1]
output_dir = sys.argv[-1]

for attr in attrs:
    list_of_rows = []
    for input_dir in input_dirs:
        rows = []
        with open(os.path.join(input_dir, attr + '.csv'), newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)
        list_of_rows.append(rows)
    
    with open(os.path.join(output_dir, attr + '.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        for rows_to_concat in zip(*list_of_rows):
            writer.writerow(sum(rows_to_concat, []))

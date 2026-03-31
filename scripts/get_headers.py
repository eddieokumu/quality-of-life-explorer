import os
import json
import glob
import csv

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    metric_dir = os.path.join(base_dir, '..', 'data', 'metric')
    
    headers_map = {}
    csv_files = glob.glob(os.path.join(metric_dir, '*.csv'))
    
    for f in csv_files:
        filename = os.path.basename(f)
        with open(f, 'r') as csvfile:
            reader = csv.reader(csvfile)
            try:
                header = next(reader)
                if len(header) > 0 and header[0] == 'id':
                    years = header[1:]
                    headers_map[filename] = years
            except StopIteration:
                pass

    out_path = os.path.join(base_dir, 'headers.json')
    with open(out_path, 'w') as outf:
        json.dump(headers_map, outf, indent=2)

if __name__ == '__main__':
    main()

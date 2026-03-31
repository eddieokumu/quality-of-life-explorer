import csv
import glob
import json

# Load the 41 Machakos IDs in order directly from the current Geography map
with open('public/data/geography/geography.geojson.json') as f:
    geo = json.load(f)

# Extract new ordered CC_3 IDs (they are already exactly ordered to match 644-684)
machakos_ids = [str(ft.get('id', ft['properties'].get('id'))) for ft in geo['features']]

# Build a straightforward sequential mapping: 644+i -> machakos_ids[i]
mapping = {}
for i, new_id in enumerate(machakos_ids):
    old_id = str(644 + i)
    mapping[old_id] = new_id

csv_files = glob.glob('data/metric/*.csv')
updated = 0

# Rewrite every single CSV to hardcode the new Machakos IDs in column 0
for file in csv_files:
    with open(file, 'rt', newline='') as f:
        reader = csv.reader(f)
        lines = list(reader)
        
    for row in lines[1:]:  # skip header
        if len(row) > 0 and row[0] in mapping:
            row[0] = mapping[row[0]]
            
    with open(file, 'wt', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(lines)
    
    updated += 1

print(f"Permanently remapped IDs in {updated} raw CSV files.")

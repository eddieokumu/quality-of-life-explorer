import json
import glob
import os

print('--- Step 1: Build Mapping ---')
with open('data/shapefiles/machakos/geography.geojson.json') as f:
    source = json.load(f)

with open('public/data/geography/geography.geojson.json') as f:
    pub = json.load(f)

old_ids = [str(f['properties']['id']) for f in pub['features']]
new_ids = []
for f in source['features']:
    cc3 = str(f['properties']['CC_3'])
    if cc3 == '0' or cc3 == 'NA':
        new_ids.append('999')
    else:
        new_ids.append(cc3)

mapping = dict(zip(old_ids, new_ids))
print(f'Constructed mapping for {len(mapping)} wards. Example: {list(mapping.items())[:5]}')

print('\n--- Step 2: Update Geography GeoJSON ---')
for f in pub['features']:
    old_id = str(f['properties']['id'])
    if old_id in mapping:
        f['properties']['id'] = str(mapping[old_id])

with open('public/data/geography/geography.geojson.json', 'w') as f:
    json.dump(pub, f)
print('Updated public/data/geography/geography.geojson.json')

print('\n--- Step 3: Update Groupings ---')
with open('src/assets/neighborhod-groups.json') as f:
    groups = json.load(f)

for category in ['Constituency', 'Municipality']:
    for group_name, wards in groups[category].items():
        new_wards = [str(mapping[str(w)]) for w in wards if str(w) in mapping]
        groups[category][group_name] = new_wards

with open('src/assets/neighborhod-groups.json', 'w') as f:
    json.dump(groups, f, indent=2)
print('Updated src/assets/neighborhod-groups.json')

print('\n--- Step 4: Update Ward Names Map ---')
with open('src/assets/ward-names.json') as f:
    ward_names = json.load(f)

new_ward_names = {}
for old_id, name in ward_names.items():
    if old_id in mapping:
        new_ward_names[str(mapping[old_id])] = name

with open('src/assets/ward-names.json', 'w') as f:
    json.dump(new_ward_names, f, indent=2)
print('Updated src/assets/ward-names.json')

print('\n--- Step 5: Update Metric JSON Files ---')
metric_files = glob.glob('public/data/metric/*.json')
updated_count = 0
for filepath in metric_files:
    with open(filepath) as f:
        data = json.load(f)
    
    dirty = False
    
    if 'map' in data:
        new_map = {}
        for old_k, v in data['map'].items():
            if str(old_k) in mapping:
                new_map[str(mapping[str(old_k)])] = v
        data['map'] = new_map
        dirty = True
        
    if 'a' in data:
        new_a = {}
        for old_k, v in data['a'].items():
            if str(old_k) in mapping:
                new_a[str(mapping[str(old_k)])] = v
        data['a'] = new_a
        dirty = True
        
    if dirty:
        with open(filepath, 'w') as f:
            json.dump(data, f)
        updated_count += 1

print(f'Successfully processed and filtered legacy data from {updated_count} metric JSON files.')


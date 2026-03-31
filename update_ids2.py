import json
import glob

with open('data/shapefiles/machakos/geography.geojson.json') as f:
    source = json.load(f)

with open('public/data/geography/geography.geojson.json') as f:
    pub = json.load(f)

# The OLD ids in pub are NOT 644 anymore. Wait, the previous script DID run.
# I need to fetch the original mapping since the previous script replaced them.
# I can rely on the fact that if a pub ID is already a new CC_3 code, it's mapped to itself.
old_pub_ids = [str(f['properties']['id']) for f in pub['features']]
new_cc3s = []
for f in source['features']:
    cc3 = str(f['properties']['CC_3'])
    new_cc3s.append('999' if cc3 in ('0', 'NA') else cc3)

# Actually, I can't build mapping from pub since pub's IDs might have been overwritten!
# Let me build mapping by ASSUMING the order in pub matches the order in source!
# It ALWAYS matched exactly in earlier checks.
mapping = {}
# For the case of metric keys, the OLD keys were 644..684.
# So let's build a manual mapping based on what we know: 644+i maps to new_cc3s[i].
for i, cc3 in enumerate(new_cc3s):
    old_id = str(644 + i)
    mapping[old_id] = cc3
    mapping[cc3] = cc3 # Identity map in case file is already updated

print("Mapping:")
print(list(mapping.items())[:5])

metric_files = glob.glob('public/data/metric/*.json')
updated = 0
for filepath in metric_files:
    with open(filepath) as f:
        data = json.load(f)
        
    dirty = False
    new_data = {}
    for k, v in data.items():
        if isinstance(v, dict) and k != 'world_val':
            # It's an id -> values dict like "m", "d", "a", "map"
            new_v = {}
            for sub_k, sub_v in v.items():
                if sub_k in mapping:
                    new_v[mapping[sub_k]] = sub_v
                    dirty = True
            new_data[k] = new_v
        else:
            new_data[k] = v
            
    if dirty:
        with open(filepath, 'w') as f:
            json.dump(new_data, f)
        updated += 1
        
print(f"Updated {updated} metric files.")

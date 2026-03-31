import os
import json
import csv
import random
import glob

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_json_path = os.path.join(base_dir, 'data', 'data.json')
    geo_json_path = os.path.join(base_dir, 'public', 'data', 'geography', 'geography.geojson.json')
    metric_dir = os.path.join(base_dir, 'data', 'metric')
    headers_json_path = os.path.join(base_dir, 'scripts', 'headers.json')

    os.makedirs(metric_dir, exist_ok=True)
    
    # Load headers mapping to maintain orig years
    with open(headers_json_path, 'r') as f:
        headers_map = json.load(f)

    # 1. Clear old CSVs
    for f in glob.glob(os.path.join(metric_dir, '*.csv')):
        os.remove(f)

    # 2. Get Geography IDs
    with open(geo_json_path, 'r') as f:
        geo_data = json.load(f)
    feature_ids = [str(feat['properties']['id']) for feat in geo_data['features'] if 'id' in feat['properties']]

    print(f"Loaded {len(feature_ids)} feature IDs from Machakos county geometry.")

    # 3. Get Metrics
    with open(data_json_path, 'r') as f:
        metrics = json.load(f)

    def write_csv(filename, data_rows, columns):
        with open(os.path.join(metric_dir, filename), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id'] + [f'y_{yr}' for yr in columns])
            for row in data_rows:
                writer.writerow(row)

    def get_years_for_metric(m_id, m_type):
        if m_type == 'mean':
            lookup = f"n{m_id}.csv"
        else:
            lookup = f"r{m_id}.csv"
        
        orig_years = headers_map.get(lookup, [])
        num_years = set()
        for y in orig_years:
            if y.startswith('y_'):
                try:
                    num_years.add(int(y.split('_')[1]))
                except ValueError:
                    pass
        
        # Ensure 1999 and 2019 are always present to satisfy census requirement
        num_years.add(1999)
        num_years.add(2019)
        return sorted(list(num_years))

    print(f"Loaded {len(metrics)} metrics. Generating Dummy Data Across Target Years...")

    for m in metrics:
        m_id = str(m['metric']).replace('m', '')
        m_type = m.get('type')
        has_accuracy = str(m.get('accuracy')).lower() == 'true'
        
        years = get_years_for_metric(m_id, m_type)

        if m_type == 'sum':
            rows_r = []
            for fid in feature_ids:
                row = [fid]
                current_val = random.randint(100, 5000)
                for i, yr in enumerate(years):
                    if i > 0: current_val = int(current_val * random.uniform(0.9, 1.2))
                    row.append(current_val)
                rows_r.append(row)
            write_csv(f'r{m_id}.csv', rows_r, years)

        elif m_type == 'mean':
            rows_n = []
            for fid in feature_ids:
                row = [fid]
                current_val = round(random.uniform(5.0, 50.0), 2)
                for i, yr in enumerate(years):
                    if i > 0: current_val = round(current_val * random.uniform(0.95, 1.05), 2)
                    row.append(current_val)
                rows_n.append(row)
            write_csv(f'n{m_id}.csv', rows_n, years)

        elif m_type == 'weighted':
            rows_r = []
            rows_d = []
            for fid in feature_ids:
                d_row = [fid]
                r_row = [fid]
                
                cur_d = random.randint(1000, 10000)
                factor = random.uniform(1.0, 100.0)
                cur_r = int(cur_d * factor)

                for i, yr in enumerate(years):
                    if i > 0:
                        cur_d = int(cur_d * random.uniform(0.95, 1.15))
                        factor = factor * random.uniform(0.9, 1.1)
                        cur_r = int(cur_d * factor)
                    d_row.append(cur_d)
                    r_row.append(cur_r)
                
                rows_d.append(d_row)
                rows_r.append(r_row)
            
            write_csv(f'r{m_id}.csv', rows_r, years)
            write_csv(f'd{m_id}.csv', rows_d, years)
            
        if has_accuracy:
            acc_rows = []
            for fid in feature_ids:
                row = [fid]
                for yr in years:
                    row.append(round(random.uniform(1.0, 10.0), 1))
                acc_rows.append(row)
            write_csv(f'm{m_id}-accuracy.csv', acc_rows, years)

    print(f"Generated data across extended years successfully.")

if __name__ == '__main__':
    main()

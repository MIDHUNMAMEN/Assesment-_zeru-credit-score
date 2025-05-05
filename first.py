import json
import csv
import os

# Load JSON from a file
with open('actual_data.json') as f:
    data = json.load(f)

# Print the contents of the "liquidations" key
print("Liquidations:", data.get("liquidations"))

# Create output directory
os.makedirs('data', exist_ok=True)

# Function to flatten nested JSON fields
def flatten_record(record):
    flat = {}
    for key, value in record.items():
        if isinstance(value, dict):
            for subkey, subval in value.items():
                flat[f"{key}_{subkey}"] = subval
        else:
            flat[key] = value
    return flat

# Export each section to CSV if it exists and is not empty
for section in ['deposits', 'borrows', 'liquidations']:
    if section in data and data[section]:
        print(f"Writing {section}.csv with {len(data[section])} records")
        records = [flatten_record(r) for r in data[section]]
        keys = records[0].keys()
        with open(f'data/{section}.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(records)
    else:
        print(f"No data found for: {section}")

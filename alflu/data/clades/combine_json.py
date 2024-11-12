import json
import os

file_names = ['1', '1a.1', '1a', '2', '2a.1', '2a.1a', '2a.1b', '2a.2', '2a.3', '2a.3a.1', '2a.3a', '2a.3b', '2a', '2b', '2c', '2d', '3C.2', '3C.2a', '3C.2a1', '3C.2a1a', '3C.2a1b.1', '3C.2a1b.1a', '3C.2a1b.1b', '3C.2a1b.2', '3C.2a1b.2a', '3C.2a1b.2b', '3C.2a1b', '3C.2a2', '3C.2a3', '3C.2a4', '3C.3', '3C.3a', '3C.3a1', '3C.3b', '3C', 'unassigned']

def merge_json(obj1, obj2):
    """
    Recursively merge two JSON objects.
    """
    if isinstance(obj1, dict) and isinstance(obj2, dict):
        merged = obj1.copy()
        for key, value in obj2.items():
            if key in merged:
                merged[key] = merge_json(merged[key], value)
            else:
                merged[key] = value
        return merged
    elif isinstance(obj1, list) and isinstance(obj2, list):
        return obj1 + obj2
    else:
        return obj2

for name in file_names:

    with open(f"ha/{name}.json") as f:
        data1 = json.load(f)
    
    with open(f"na/{name}.json") as f: 
        data2 = json.load(f)

    #data1.update(data2) 

    #with open(f"{name}.json", 'w') as f:
    #   json.dump(data1, f)
    # Merge data from both files
    merged_data = merge_json(data1, data2)

    # Write merged data to a new JSON file
    with open(f"{name}.json", 'w') as f:
        json.dump(merged_data, f, indent=4)  # indent for readability

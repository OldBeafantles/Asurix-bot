import json

def load_json(filename : str):
    with open(filename, encoding = "utf-8", mode = "r") as f:
        data = json.load(f)
    return data

def save_json(data : json, filename : str, sorted = True):
    with open(filename, encoding = "utf-8", mode = "w") as f:
        json.dump(data, f, indent = 4, sort_keys = sorted, separators = (',', ': '))
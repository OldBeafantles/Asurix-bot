"""Utilities functions file"""
import json

def load_json(filename: str):
    """Loads a json file"""
    with open(filename, encoding="utf-8", mode="r") as file:
        data = json.load(file)
    return data

def save_json(data: json, filename: str, should_be_sorted=True):
    """Saves a json file"""
    with open(filename, encoding="utf-8", mode="w") as file:
        json.dump(data, file, indent=4, sort_keys=should_be_sorted, separators=(',', ': '))
        
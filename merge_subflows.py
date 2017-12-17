#!/usr/bin/env python3
''' take all files from the cwd and merge them into a master flows.json
'''
import glob
import json

if __name__ == "__main__":

    glob_data = []
    for file in glob.glob('subflows/subflow_*.json'):
        with open(file) as json_file:
            data = json.load(json_file)

            i = 0
            while i < len(data):
                glob_data.append(data[i])
                i += 1

    with open('data/flows.json', 'w') as f:
        json.dump(glob_data, f, indent=4)

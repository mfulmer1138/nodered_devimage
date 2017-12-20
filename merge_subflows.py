#!/usr/bin/env python3
''' take all files from the subflows directory under the current working directory
    and merge them into a master flows.json
'''

import glob
import json

__author__ = "Michael Fulmer"
__copyright__ = "Copyright (C) 2017 Michael Fulmer"
__license__ = "MIT License"
__version__ = "1.0"

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

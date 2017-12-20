#!/usr/bin/env python3
''' utility class to create project based on current nodered_devimage state
    performs the following actions:
    - [ ] create directory structure with the following files
            .
            +-- nodered_devimage/
            +-- new_container/
                +-- .gitignore - created as noted below
                +-- Dockerfile - created as noted below
                +-- LICENSE - created as noted below
                +-- README.md - created as noted below
                +-- supporting files - created as noted below
                +-- data/
                    +-- flows.json - created as noted below
                    +-- settings.js - created as noted below
    - [ ] Dockerfile
            cp Dockerfile from nodered_devimage
            Requires that Dockerfile has been modified to contain new standard
            or container specific npm installs.
            At a minimum, the content will be:
                FROM nodered/node-red-docker
                COPY data/flows.json /data
                COPY data/settings.js /data
    - [ ] supporting files
            cp all files that are not contained in root of the base nodered_devimage repo
    - [ ] data/flows.json
            cp flows.json from nodered_devimage/data
    - [ ] data/settings.js
            cp settings.js from nodered_devimage/data
            Requires that settings.js has been modified to contain new standard
            or container specific settings/requires
    - [ ] .gitignore
            Only exclude OS specific adds (e.g., DS_Stores)
    - [ ] LICENSE
            MIT License with current user's name from git config
    - [ ] README.md
            Blank README, to be editted post container structure creation
'''
import sys
import getopt

__author__ = "Michael Fulmer"
__copyright__ = "Copyright (C) 2017 Michael Fulmer"
__license__ = "MIT License"
__version__ = "1.0"

def usage():
    u = "{} -n <name> -d <dir>\n"\
        "\n"\
        "    -n, --name=<name> ... the name of the container and directory name to house the container\n".format(sys.argv[0])
    return u

if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h?n:d:", ["name="])
    except getopt.GetoptError as err:
        print(err)
        print(usage())
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or opt == '-?':
            print(usage())
            sys.exit()
        elif opt in ("-n", "--n"):
            container_name = arg

    # TODO: add requirements above

    raise Exception("Application not functional currently")

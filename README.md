# node-red development image

Run `./setup.sh` to create data directory, merge all subflows into the default flows.json, and build the container

Run the container (with suggested port 8080):
``` sh
docker run -it -p 8080:1880 --rm -v /absolute/path/to/devimage/data/:/data -d --name devimage devimage:latest
```

Proceed to build flows and subflows as required.

When the flows are ready for container deployment, the flows.json file will need to be copied to the data directory of the final conainter by copying the flows.json to a local data folder in the root of your new container project and including `COPY data/flows.json /data` in the Dockerfile. For example:
``` Dockerfile
FROM nodered/node-red-docker
COPY data/flows.json /data
```

If new packages are required for the new flows, the Dockerfile of the new container must contain the npm directives. For example:
``` Dockerfile
FROM nodered/node-red-docker
RUN npm install node-red-contrib-env
COPY data/flows.json /data
```

If new subflows are created during the process of the flow development, and these subflows are deemed a shareable asset by the team, the subflows must be exported by using the `export_subflows.py` Python 3 script and a pull request for the devimage must be initiated to merge the new subflows into the devimage repo.

Usage for export_subflows.py:
```
./export_subflows.py -u <url> -d <dir>'.format(sys.argv[0])

    -u, --url=<url> ... the base url for the devimage container, typically '8080'
    -d, --dir=<dir> ... the directory to output the subflows, typically 'subflows'
```

Lastly, if the new subflows require new pacakges, the master Dockerfile for this repo must include the npm directives. Again, a pull request must be initiated to merge these Docker file changes into the devimage repo.

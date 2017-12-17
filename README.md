# node-red development image

Run `./setup.sh` to create data directory, cp subflow master json file in as the default flows.json, and build the container

Run the container (with suggested port 8080):
``` sh
docker run -it -p 8080:1880 --rm -v /absolute/path/to/devimage/data/:/data -d --name devimage devimage:latest
```

Proceed to build flows and subflows.

When flow is ready, the flow will be copied to the data directory of the final conainter by copying the flows.json to the local data folder of your new container project and including `COPY data/flows.json /data` in the Dockerfile.

If new packages are required for the new flow, the Dockerfile of the new container must contain the npm directives. For example:
``` Dockerfile
FROM nodered/node-red-docker
RUN npm install node-red-contrib-env
COPY data/flows.json /data
```

If new subflows are created, in addition to copying the resulting flows.json file into the new container, the new subflows and subflows_master.json file must be updated into the subflows folder of this repo. This process is achieved with the `export_subflows.py` script.

Lastly, if the new subflows require new pacakges, the master Dockerfile for this repo must include the npm directives.

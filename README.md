# node-red development image

This repo contains an example Docker mangaged Node-RED deployment used for developing flows intended to run as isolated Docker containers. Additionally, the repo contains the mechanisms necessary to share subflow development across a team or organization.

A typical project directory structure for working with both the devimage container and the new service containers looks as follows:
```
.
+-- nodered_devimage
|   +-- Dockerfile
|   +-- export_subflows.py
|   +-- manage_subflows.py
|   +-- setup.sh
|   +-- data
|   |   +-- flows.json
|   +-- subflows
|       +-- subflow_example.json
+-- new_container
    +-- Dockerfile
    +-- other supporting files
    +-- data
        +-- flows.json
```

Run `./setup.sh` to create data directory, merge all subflows into the default `flows.json`, and build the container. This setup script will call the `merge_flows.json` script to build `flows.json` from the individual subflow scripts found in the `subflows` directory. The container build is executed with the following arguments: 
```sh
docker build -t devimage:latest .
```

Run the container (with suggested port 8080):
```sh
docker run -it -p 8080:1880 --rm -v /absolute/path/to/devimage/data/:/data -d --name devimage devimage:latest
```

Connect to the container (typically [http://127.0.0.1:8080](http://127.0.0.1:8080) for the typical local container installation) and proceed to build flows and subflows as required.

When the flows are ready for container deployment, the `flows.json` file will need to be copied to the `data` directory of the final conainter by copying the flows.json to a `data` directory in the root of your new container project and including `COPY data/flows.json /data` in the `Dockerfile`. For example:
```Dockerfile
FROM nodered/node-red-docker
COPY data/flows.json /data
```

If new packages are required for the new flows, the `Dockerfile` of the new container must contain the `npm` directives. For example:
```Dockerfile
FROM nodered/node-red-docker
RUN npm install node-red-contrib-env
COPY data/flows.json /data
```

If new subflows are created during the process of the flow development, and these subflows are deemed a shareable asset by the team, the subflows must be exported by using the `export_subflows.py` Python 3.5+ script and a pull request for the `devimage` must be initiated to merge the new subflows into the `devimage` repo.

Usage for `export_subflows.py`:
```
./export_subflows.py -u <url> -d <dir>

    -u, --url=<url> ... the base url for the devimage container, typically 'http://127.0.0.1/8080'
    -d, --dir=<dir> ... the directory to output the subflows, typically 'subflows'
```

Lastly, if the new subflows require new pacakges, the master `Dockerfile` for this repo must include the `npm` directives. Again, a pull request must be initiated to merge these `Dockerfile` changes into the `devimage` repo.

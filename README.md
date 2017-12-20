# node-red development image

This repo contains an example Docker mangaged Node-RED deployment used for developing flows intended to run as isolated Docker containers. Additionally, the repo contains the mechanisms necessary to share subflow development across a team or organization. :rocket: 

**_TODO:_** 
 - [ ] Create a "build new container" script that will create the baseline Dockerfile and move the flow.json file and setting.js file. Currently this must be done manually, using the recommendations below.

A typical project directory structure for working with both the `devimage` container and the new service containers looks as follows:
```
.
+-- nodered_devimage
|   +-- Dockerfile
|   +-- export_subflows.py
|   +-- manage_subflows.py
|   +-- setup.sh
|   +-- data
|   |   +-- flows.json
|   |   +-- settings.js
|   +-- subflows
|       +-- subflow_example1.json
|       +-- subflow_exmaple2.json
+-- new_container
    +-- Dockerfile
    +-- other supporting files
    +-- data
        +-- flows.json
        +-- settings.js
```

Run `./setup.sh` merge all subflows into the default `flows.json` and build the `devimage` container. This setup script will call the `merge_flows.json` script to build `flows.json` from the individual subflow scripts found in the `subflows` directory and place the `flows.json` file into the `data` directory of `nodered_devimage`. The container build is executed with the following arguments: 
```sh
docker build -t devimage:latest .
```

Run the container (with suggested port 8080):
```sh
docker run -it -p 8080:1880 --rm -v /absolute/path/to/nodered_devimage/data/:/data -d --name devimage devimage:latest
```

Connect to the container (typically [http://127.0.0.1:8080](http://127.0.0.1:8080) for the typical local container installation) and proceed to build flows and subflows as required.

When the flows are ready for container deployment, the `flows.json` and `settings.js` file will need to be copied to the `data` directory of the final conainter by copying thes files to a `data` directory in the root of your new container project and including `COPY` directives in the `Dockerfile`. For example:
```sh
# from the nodered_devimage directory
cp ./data/flows.json ../new_container/data
cp ./data/settings.json ../new_container/data
```
and
```Dockerfile
FROM nodered/node-red-docker
COPY data/flows.json /data
COPY data/settings.js /data
```

If new packages are required for the new flows, the `Dockerfile` of the new container must contain the `npm` directives. For example:
```Dockerfile
FROM nodered/node-red-docker
RUN npm install node-red-contrib-env
COPY data/flows.json /data
COPY data/settings.js /data
```

If new subflows are created during the process of the flow development, and these subflows are deemed a shareable asset by the team, the subflows must be exported by using the `export_subflows.py` Python 3.5+ script and a pull request must be initiated to merge the new subflows into the `nodered_devimage` repo.

Usage for `export_subflows.py`:
```
./export_subflows.py -u <url> -d <dir>

    -u, --url=<url> ... the base url for the devimage container, typically 'http://127.0.0.1/8080'
    -d, --dir=<dir> ... the directory to output the subflows, typically 'subflows'
```

If the new subflows require new Node-RED pacakges, the master `Dockerfile` for this repo must include the `npm` directives. Again, a pull request must be initiated to merge these `Dockerfile` changes into the `nodered_devimage` repo.

If the new flows or subflows require new Node packages (these would be packages added to function scripts via the `var packagename = global.get('<packagename>');` call), the settings.js file must be modified to include these pacakges in the global context. Examples of modification are included in the settings.js file as well as here:
```
    functionGlobalContext: {
        // os:require('os'),
        // octalbonescript:require('octalbonescript'),
        // jfive:require("johnny-five"),
        // j5board:require("johnny-five").Board({repl:false}),
        packagename:require('<packagename>')
    },
 ```

Additionally, the `Dockerfile` must include the `npm` directive for installing the new package. For example:
```Dockerfile
FROM nodered/node-red-docker
RUN npm install <packagename>
COPY data/flows.json /data
COPY data/settings.js /data
```

A pull request must be initiated to merge any `settings.js` changes for subflows into the `nodered_devimage` repo. If the changes are specific to a flow, then the pull request is not necessary.

Lastly, if, during the course of flow development, you are required to develop a new Node-RED node, please follow the instructions found here: [https://nodered.org/docs/creating-nodes/](https://nodered.org/docs/creating-nodes/), paying special attention to the packaging and npm publishing instructions. Packages built this way will be included in the containers via the `RUN npm install <pacakagename>` directive in the `Dockerfile`. An example package can be found here: [https://flows.nodered.org/node/node-red-contrib-csvtojson](https://flows.nodered.org/node/node-red-contrib-csvtojson).

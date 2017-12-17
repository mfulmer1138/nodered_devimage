#!/usr/bin/env python3
''' utility class to support impoort and export of subflows
'''

from urllib.parse import urlparse
import json
import requests

class Flows(object):
    ''' main Flows utility class
    '''
    def __init__(self):
        self.__flows = None
        self.__url = None

    def set_flows(self, url):
        ''' takes a node-red url scheme, host, and port then sets internal object with result of
        the "flows" api GET request
        '''
        if url[:4] != "http" and url[:2] != "//":
            url = "//" + url
        self.__url = urlparse(url, "https")
        flows_url = "{}://{}:{}/flows".format(
            self.__url.scheme, self.__url.hostname, self.__url.port)
        print(flows_url)
        req = requests.get(flows_url)
        self.__flows = json.loads(req.text)

    def get_flows(self):
        ''' returns contents of flows file as python object
        '''
        return self.__flows

    def iterate_subflows(self):
        ''' iterator to return all ids and names, as a tuple, associated with subflows
        '''
        for element in self.__flows:
            if element["type"] == "subflow":
                yield (element["id"], element["name"])

    def get_id(self, name):
        ''' takes a subflow name as a string and returns the id
        '''
        for element in self.__flows:
            if element["type"] == "subflow" and element["name"] == name:
                return element["id"]

    def get_subflow(self, subflow_id):
        ''' takes a subflow id as a string and returns the json elements required for the subflow
        '''
        subflow = []
        for element in self.__flows:
            if element["type"] == "subflow" and element["id"] == subflow_id:
                subflow.append(element)
            elif "z" in element and element["z"] == subflow_id:
                subflow.append(element)
        return subflow

    def get_subflows(self):
        ''' return only the elements associated with subflows
        '''
        subflows = []
        for (sid, name) in self.iterate_subflows():
            subflows.extend(self.get_subflow(sid))
        return subflows

    def store_subflow(self, subflow, name):
        ''' takes a subflow object and a file path and name and writes the object as a json string
        '''
        with open(name, "w") as flows_file:
            flows_file.write(json.dumps(subflow, indent=4))

if __name__ == "__main__":
    flows = Flows()
    flows.set_flows("http://127.0.0.1:1880/")

    for (sid, name) in flows.iterate_subflows():
        subflow = flows.get_subflow(sid)
        flows.store_subflow(subflow, "./flows/subflow_{}.json".format(name.replace(" ", "_")))

    flows.store_subflow(flows.get_subflows(), "./flows/subflow_master.json")
    flows.store_subflow(flows.get_flows(), "./flows/flow_master.json")

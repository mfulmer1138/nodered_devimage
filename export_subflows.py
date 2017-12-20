#!/usr/bin/env python3
''' utility class to support impoort and export of subflows
'''

from urllib.parse import urlparse
import sys
import getopt
import json
import requests

__author__ = "Michael Fulmer"
__copyright__ = "Copyright (C) 2017 Michael Fulmer"
__license__ = "MIT License"
__version__ = "1.0"

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

def usage():
    u = "{} -u <url> -d <dir>\n"\
        "\n"\
        "    -u, --url=<url> ... the base url for the devimage container, typically 'http://127.0.0.1/8080'\n"\
        "    -d, --dir=<dir> ... the directory to output the subflows, typically 'subflows'\n".format(sys.argv[0])
    return u

if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h?u:d:", ["url=", "dir="])
    except getopt.GetoptError as err:
        print(err)
        print(usage())
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or opt == '-?':
            print(usage())
            sys.exit()
        elif opt in ("-u", "--url"):
            url = arg
        elif opt in ("-d", "--dir"):
            outdir = arg


    flows = Flows()
    flows.set_flows(url)

    for (sid, name) in flows.iterate_subflows():
        subflow = flows.get_subflow(sid)
        flows.store_subflow(subflow, "{}/subflow_{}.json".format(outdir, name.replace(" ", "_")))

    # examples of other features
    #flows.store_subflow(flows.get_subflows(), "./flows/subflow_master.json")
    #flows.store_subflow(flows.get_flows(), "./flows/flow_master.json")

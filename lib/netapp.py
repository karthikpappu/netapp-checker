import configparser
import requests
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Netapp (object):
    def __init__(self):
        self.dir = os.path.dirname(__file__)
        config = configparser.ConfigParser()
        self.config = config
        self.config.read(os.path.join(self.dir, "../config.ini"))
        self.url = self.config.get("default", "url")
        self.ver = self.config.get("default", "ver")
        self.apitype = self.config.get("default", "apitype")
        self.apiuser = self.config.get("default", "apiuser")
        self.apipass = self.config.get("default", "apipass")

    def apiget(self, apiroute):
        apiurl = self.url + "/{}/{}/{}".format(self.ver, self.apitype, apiroute)
        apireq = requests.get(apiurl, auth=(self.apiuser, self.apipass), verify=False)
        return apireq.json()

    def getallnodesinfo(self):
        """
        Return all nodes from netappAPI service
        :return: list
        """
        apireq = self.apiget("nodes")
        return apireq["result"]["records"]

    def getnodeinfo(self, node):
        """
        Return info from specific node
        :param node:
        :return: dict
        """
        nodes = self.getallnodesinfo()
        for n in nodes:
            if node in n["name"]:
                return n
        raise ValueError("Host not found, no value return")

    def getnodemetrics(self, host, mode=None):
        node = self.getnodeinfo(host)
        apicall = "nodes/metrics?resource_key={}".format(node["key"])
        apireq = self.apiget(apicall)
        metric = apireq["result"]["records"][0]["metrics"]
        if mode == "print":
            for i in range(len(metric)):
                print("\t", metric[i]["name"], ":", metric[i]["samples"][0]["value"], metric[i]["unit"], "at", metric[i]["samples"][0]["timestamp"])
        else:
            return metric


    def getallaggregates(self):
        """
        Return all aggregates from netappAPI service
        :return: list
        """
        apireq = self.apiget("aggregates")
        return apireq["result"]["records"]

    def getaggregatesbycluster(self, clusterkey):
        """
        Return aggregates by clusterkey from netappAPI service
        :return:
        """
        apicall = "clusters/{}/aggregates".format(clusterkey)
        apireq = self.apiget(apicall)
        return apireq["result"]["records"]

    def getaggregatesbynode(self, nodekey):
        apicall = "nodes/{}/aggregates".format(nodekey)
        apireq = self.apiget(apicall)
        return apireq["result"]["records"]

    def getvolumesbyaggr(self, aggrkey):
        """
        Return all volumes of an aggregates from netappAPI service
        :param aggrkey:
        :return: list
        """
        apicall = "aggregates/{}/volumes".format(aggrkey)
        apireq = self.apiget(apicall)
        return apireq["result"]["records"]

    def getnode(self, nodekey):
        apicall = "nodes/{}".format(nodekey)
        apireq = self.apiget(apicall)
        return apireq["result"]["records"]

    def getallclusters(self):
        apireq = self.apiget("clusters")
        return apireq["result"]["records"]

    def getclusterinfo(self, clusterkey):
        apicall = "clusters/{}".format(clusterkey)
        apireq = self.apiget(apicall)
        return apireq["result"]["records"][0]

    def showallitems(self, ditem, tabn):
        for k, v in ditem.items():
            print("\t" * tabn, "{} => {}".format(k, v))

    def printnodemetric(self, nodekey):
        apicall = "nodes/metrics?resource_key={}".format(nodekey)
        apireq = self.apiget(apicall)
        metric = apireq["result"]["records"][0]["metrics"]
        for i in range(len(metric)):
            print("\t", metric[i]["name"], ":", metric[i]["samples"][0]["value"], metric[i]["unit"], "at", metric[i]["samples"][0]["timestamp"])

    def printallinfos(self, nodes=None):
        if nodes is None:
            nodes = self.getallnodesinfo()
        for node in nodes:
            nodename = node["name"]
            clusterkey = node["cluster_key"]
            cluster = self.getclusterinfo(clusterkey)
            print("CLUSTER NAME = ", cluster["name"])
            print("-" * 40)
            print("HOST =>", nodename)
            self.showallitems(node, 1)
            self.printnodemetric(node["key"])
            aggregates = self.getaggregatesbycluster(clusterkey)
            for aggregate in aggregates:
                aggrname = aggregate["name"]
                aggrkey = aggregate["key"]
                print("AGGREGATES INFO =>")
                self.showallitems(aggregate, 2)
                print()
                volumes = self.getvolumesbyaggr(aggrkey)
                print("\tAGGR NAME =>", aggrname)
                for v in range(len(volumes)):
                    if volumes[v]["vol_type"] != "dp":
                        print("\t\tVolume Name ->", volumes[v]["name"])
                        print("\t\t\tPercent used", volumes[v]["size_used_percent"])
                        print("\t\t\tPercent Avail", volumes[v]["size_avail_percent"])
                        print("\t\t\tSize used in Byte", volumes[v]["size_used"])
                        print("\t\t\tState", volumes[v]["state"])
            print("-" * 40)
            break

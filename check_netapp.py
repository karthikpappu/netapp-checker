#!/usr/bin/python3

from lib.netapp import Netapp
import argparse
import json
import sys


class NetappChecker (object):
    def __init__(self):
        self.modes = {
            "nodeperf": self.nodeperf,
            "aggrperf": self.storageperf,
            "volumeperf": self.storageperf,
            "healthmode": self.healthmode,
        }
        self.types = {
            "ha": "ha_",
            "network": "net_",
            "cpu_busy": "cpu_busy",
            "cpu_elapsed_time": "cpu_elapsed_time",
            "ops": "_ops",
            "nfs": "nfs_",
            "throughput": "throughput",
            "fcp": "fcp_",
            "system": "sys_",
        }
        self.netapp = Netapp()

    def argument(self):
        self.parser = argparse.ArgumentParser(prog="check_netapp", description="Netapp check plugins for icinga2")
        self.parser.add_argument('-H', dest='host', type=str, help="Hostname or cluster to check", required=True)
        self.parser.add_argument('-w', dest='warning', type=int, default=0, help="Warning level")
        self.parser.add_argument('-c', dest='critical', type=int, default=0, help="Critical level")
        self.parser.add_argument('-d', dest='disk', type=str, help="Disk")
        self.parser.add_argument('-u', dest='unit', type=str, help="unit to display ( %, bytes)")
        self.parser.add_argument('-n', dest='name', type=str, help="name of volume you wanna check")
        self.parser.add_argument('-t', dest='metrictype', type=str, help="Choose the type of metric you wanna return "
                                                                         "( ha, network, cpu_busy, cpu_elapsed_time, ops,"
                                                                         " nfs, throughput, fcp, system )")
        self.parser.add_argument('-m', dest='mode', type=str, help="Type of mode for checking netapp host or cluster Mode:"
                                                                   " ( nodeperf {combine with metrictype}, healthmode)",
                                 required=True)
        self.parser.add_argument('-v', dest='verbose',action='store_true', help="verbose")
        self.args = self.parser.parse_args()

        if self.args.mode not in self.modes \
                or self.args.mode == "nodeperf" and self.args.metrictype is None:
            print(self.parser.format_help())
            exit(1)

    def printoutput(self, dstatus):
        print(dstatus["status_type"], " ".join(map(str, dstatus["msg"])), "|", " ".join(map(str, dstatus["perfdata"])))

    def checkstatus(self, lperf):
        """
        Give list perf and give final status
        :param lperf:
        :return:
        """
        gstatus = dict()
        gstatus["status"] = int()
        gstatus["status_type"] = str()
        gstatus["msg"] = list()
        gstatus["perfdata"] = list()
        for i in range(len(lperf)):
            if lperf[i]["status"] <= 0 and gstatus["status"] <= 0:
                gstatus["status"] = 0
                gstatus["status_type"] = "OK"
            elif lperf[i]["status"] <= 1 and gstatus["status"] <= 1:
                gstatus["status"] = 1
                gstatus["status_type"] = "WARNING"
            elif lperf[i]["status"] <= 2 and gstatus["status"] <= 2:
                gstatus["status"] = 2
                gstatus["status_type"] = "CRITICAL"
            elif lperf[i]["status"] <= 3 and gstatus["status"] <= 3:
                gstatus["status"] = 3
                gstatus["status_type"] = "UNKNOWN"
            gstatus["perfdata"].append(lperf[i]["perfdata"])

        for i in range(len(lperf)):
            if gstatus["status"] == lperf[i]["status"]:
                gstatus["msg"].append(lperf[i]["msg"])

        return gstatus

    def nagiosperdata(self, label, value, warn, crit, max=None):
        if max:
            nagiosperfdata = "{}={};{};{};{};{}".format(label, value, warn, crit, 0, max)
        else:
            nagiosperfdata = "{}={};{};{}".format(label, value, warn, crit)
        return nagiosperfdata

    def nagiosstatus(self, msg, warn, crit, status=None, **kwargs):
        output = {
            "msg": msg,
            "status": status
        }

        # if maxvalue in perfdata make percent out of it
        if "value" in kwargs:
            if len(str(kwargs["value"])) > 3 and "maxvalue" in kwargs:
                crit = (kwargs["maxvalue"] * crit) / 100
                warn = (kwargs["maxvalue"] * warn) / 100


        if status is None and warn and crit:
            if warn > kwargs["value"]:
                output["status"] = 0
            elif warn <= kwargs["value"] and crit > kwargs["value"]:
                output["status"] = 1
            elif crit <= kwargs["value"]:
                output["status"] = 2
        else:
            output["status"] = 0

        if output["status"] is 0:
            output["msg"] = "{}".format(msg)
        elif output["status"] is 1:
            output["msg"] = "{}".format(msg)
        elif output["status"] is 2:
            output["msg"] = "{}".format(msg)
        elif output["status"] is 3:
            output["msg"] = "{}".format(msg)
        if kwargs:
            if "maxvalue" in kwargs:
                nagiosperfdata = self.nagiosperdata(msg, kwargs["value"], warn, crit, kwargs["maxvalue"])
            else:
                nagiosperfdata = self.nagiosperdata(msg, kwargs["value"], warn, crit)
            output.update({"perfdata": nagiosperfdata})
        else:
            print(output["msg"])
            exit(output["status"])

        return output

    def nodeperf(self, host, metrictype=None):
        metrics = self.netapp.getnodemetrics(host)
        crit = self.args.critical
        warn = self.args.warning
        result = []
        for n in range(len(metrics)):
            metname = metrics[n]["name"]
            metunit = metrics[n]["unit"]
            metvalue = metrics[n]["samples"][0]["value"]
            if self.types[self.args.metrictype] in metrics[n]["name"]:
                result.append(self.nagiosstatus("{}.{}".format(metrics[n]["name"], metunit), warn, crit, label=metname, value=metvalue, unit=metunit))
        # this is for testing purpose
        if self.args.verbose:
            for i in range(len(result)):
                print(result[i])

        gstatus = self.checkstatus(result)
        self.printoutput(gstatus)
        exit(gstatus["status"])

    def returnperf(self, perfdict):
        metname = perfdict.get("name")
        if self.args.unit == "%":
            valueunit = "in_perc"
            metvalue = perfdict.get("size_used_percent")
            metvaluemax = 0
        elif self.args.unit == "bytes":
            valueunit = "bytes"
            metvalue = perfdict.get("size_used")
            metvaluemax = perfdict.get("size_total")

        return self.nagiosstatus("{}.{}".format(metname, valueunit), self.args.warning, self.args.critical,
                                 None, label=metname, value=metvalue,
                                 maxvalue=metvaluemax, unit=self.args.unit)


    def storageperf(self, host):
        hostinfo = self.netapp.getnodeinfo(host)
        agrrs = self.netapp.getaggregatesbynode(hostinfo["key"])
        result = []
        if self.args.mode == "aggrperf":
            for n in agrrs:
                result.append(self.returnperf(n))
        elif self.args.mode == "volumeperf":
            for i in agrrs:
                vols = self.netapp.getvolumesbyaggr(i.get("key"))
                if not self.args.name:
                    for vol in vols:
                        result.append(self.returnperf(vol))
                else:
                    for vol in vols:
                        if vol.get("name") == self.args.name:
                            result.append(self.returnperf(vol))

        gstatus = self.checkstatus(result)
        self.printoutput(gstatus)
        exit(gstatus["status"])


    def healthmode(self, host):
        """
        Get health status for a node
        :param host:
        :return: stdout string
        """
        node = self.netapp.getnodeinfo(host)
        warn = self.args.warning
        crit = self.args.critical
        if not node:
            self.nagiosstatus("Host {} not find".format(host), warn, crit, 3)
            print(self.parser.format_help())
        if not node["is_node_healthy"]:
            self.nagiosstatus("node is unhealthy", warn, crit, 1)
            print("REPORT:")
            print(self.netapp.showallitems(node, 1))
        else:
            self.nagiosstatus("Host {} is healthy !".format(host), warn, crit, 0)

    def __call__(self, *args, **kwargs):
        self.argument()
        self.modes[self.args.mode](self.args.host)

if __name__ == '__main__':
    check = NetappChecker()
    check()
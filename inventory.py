#!/usr/bin/python3

from lib.netapp import Netapp
import argparse


if __name__ == '__main__':
    netapp = Netapp()
    netapp.printallinfos()
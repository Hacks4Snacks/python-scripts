#!/bin/env python3
# simple script to perform an ARP ping on a network

from scapy.all import *
import sys
import os
import ipaddress

def prerun_test():

    if not os.geteuid() == 0:
        sys.exit('This script must be run as root.')

    if len(sys.argv) != 2:
        print(f'Usage: arp_ping.py <network>')
        print(f'Example: ./arp_ping.py 192.168.1.0/24')
        sys.exit(1)

    try:
        ip_network = ipaddress.ip_network(sys.argv[1]) # is argv a valid IP or IP/CIDR combination
    
    except ValueError:
        print(f'{sys.argv[1]} is an invalid IP network')
        print(f'Usage: arp_ping.py <network>')
        sys.exit(f'Example: ./arp_ping.py 192.168.1.0/24')


def arp_ping(network):

    conf.verb = 0

    ans, unans = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=sys.argv[1]), timeout=2)

    print("MAC ADDRESS       IP ADDRESS")

    for s,r in ans:
        print(r.sprintf("%Ether.src% %ARP.psrc%"))

def main():
    prerun_test()
    arp_ping(sys.argv[1])

if __name__ == '__main__':
    main()

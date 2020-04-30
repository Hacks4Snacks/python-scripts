#!/bin/env python3
# simple script to perform an ARP ping on a network

from scapy.all import *
import sys

if len(sys.argv) != 2:
    print(f'Usage: arp_ping.py <network>')
    print(f'Example: ./arp_ping.py 192.168.1.1/24')
    sys.exit(1)

conf.verb = 0

ans, unans = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=sys.argv[1]), timeout=2)

print("MAC ADDRESS       IP ADDRESS")

for s,r in ans:
    print(r.sprintf("%Ether.src% %ARP.psrc%"))

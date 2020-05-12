#!/bin/env python3

# simple script to get a range of IPs from a CIDR address.

import ipaddress
import sys

def prerun():
    
    if len(sys.argv) != 2:
        print(f'Usage: ip_cidr_lookup.py <network range>')
        print(f'Example: ./ip_cidr_lookup.py 192.168.1.0/24')
        sys.exit(1)

    try:
        ip_network = ipaddress.ip_network(sys.argv[1]) # is argv a valid IP or IP/CIDR combination

    except ValueError:
        print(f'{sys.argv[1]} is an invalid IP network')
        print(f'Usage: ip_cidr_lookup.py <network>')
        sys.exit(f'Example: ip_cidr_lookup.py 192.168.1.0/24')
    
def get_ip():
    
    ip_network = ipaddress.ip_network(sys.argv[1])
    for ip in ip_network:
        print(ip)

def main():
    prerun()
    get_ip()

if __name__ == '__main__':
    main()

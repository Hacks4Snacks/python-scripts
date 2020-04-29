#!/bin/env python3
# simple script to review disk usage

import shutil

total_b, used_b, free_b = shutil.disk_usage('.')

gib = 2 ** 30 # GiB == gibibyte
gb = 10 ** 9 # GB == gigabyte

print(f'Total: {total_b /gib :6.2f} GiB  {total_b /gb :6.2f} GB')
print(f'Used:  {used_b / gib :6.2f} GiB  {used_b / gb :6.2f} GB')
print(f'Free:  {free_b / gib :6.2f} GiB  {free_b / gb :6.2f} GB')

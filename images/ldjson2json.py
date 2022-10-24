#!/usr/bin/env python3
"""
Converts ldjson to json array
"""
import json
import sys


lines = []
for l in sys.stdin:
    lines.append(json.dumps(json.loads(l)))

print("[")

for l in lines[0:-1]:
    print(l + ",")

print(lines[-1])
print("]")

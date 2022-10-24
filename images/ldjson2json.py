#!/usr/bin/env python3
"""
Converts ldjson to json array
"""
import json
import sys


lines = []
errors = 0
for l in sys.stdin:
    try:
        lines.append(json.dumps(json.loads(l)))
    except:
#        print("error line", l)
        errors += 1

print("[")

for l in lines[0:-1]:
    print(l + ",")

print(lines[-1])
print("]")

#print(errors)

#!/bin/env python3

import time
from datetime import datetime

now=datetime.now().timestamp()

print(f"Now is:         {int(now)}")

then=int(input("Enter timestamp %d/%m/%y %H:%M:"))
thenString = datetime.fromtimestamp(then).strftime("%d/%m/%y %H:%M")

s = then-now



print(f"This will be on {thenString}")
print(f"{int(s)} seconds until then")
print(f"{int(s/60/60)} hours until then")
print(f"{int(s/60/60/24)} days until then")

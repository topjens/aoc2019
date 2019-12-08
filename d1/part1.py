# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 06:11:08 2019

@author: Jens
"""

import math

total = 0

with open("input") as input:
    for line in input:
        total += math.floor(int(line)/3) - 2
        
print(total)
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 06:11:08 2019

@author: Jens
"""

import math

total = 0

with open("input") as input:
    for line in input:
        module = math.floor(int(line)/3) - 2
        
        added_mass = module
        
        while(added_mass > 0):
            added_mass = math.floor(added_mass/3) - 2
            if(added_mass > 0):
                module += added_mass
                
        total += module
        
print(total)
        
#        
#print(total)
#
#subtotal = total
#
#while(subtotal > 0):
#    subtotal = math.floor(subtotal/3) - 2
#    if(subtotal > 0):
#        total += subtotal
#    
#print(total)
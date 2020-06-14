#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 05:24:54 2020

@author: deepak
"""

from blowfish import Blowfish
from time import time

#create object and initialize blowfish with 8 keys (parameter 1) and no. of keys (parameter 2)
bf = Blowfish()
key = 'This is a key'
key_array = [ord(x) for x in key]
t = time.time()
bf.initialize_blowfish(key_array,len(key_array))
print(time.time()-t)

print("time to encrypt = ",bf.encrypt_image("Mahi.jpeg", 4))


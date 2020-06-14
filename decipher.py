#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 03:14:24 2020

@author: deepak
"""

from blowfish import *   
import time

#create object and initialize blowfish with 8 keys (parameter 1) and no. of keys (parameter 2)
bf = Blowfish()
key = 'This is a key'
key_array = [ord(x) for x in key]
t = time.time()
bf.initialize_blowfish(key_array,len(key_array))
print(time.time()-t)

print("time to decrypt = ",bf.decrypt_image("enciphered_image.jpeg",2))
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 05:24:54 2019

@author: deepak
"""

from Blowfish import *

#create object and initialize blowfish with 8 keys (parameter 1) and no. of keys (parameter 2)
bf = Blowfish()
bf.initializeBlowfish([1,2,3,4,5,6,7,8],8)

print("time to encrypt = ",bf.encrypt_image("image_to_encrypt.jpeg"))


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 03:14:24 2019

@author: deepak
"""

from Blowfish import *   

#create object and initialize blowfish with 8 keys (parameter 1) and no. of keys (parameter 2)
bf = Blowfish()
bf.initializeBlowfish([1,2,3,4,5,6,7,8],8)

print("time to decrypt = ",bf.decrypt_image("enciphered_image.jpeg"))
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 7:14:24 2020

@author: deepak
"""

from helper import Helper

inp = int(input("Press:\n1. Encipher\n2. Decipher\n=>"))
if (inp==1):
    image_path = input("Please input image path:")
    key = input("Please input key:")
    no_of_cores = int(input("Please input number of cores:"))
    print("Processing...")
    Helper.encipher(image_path, key, no_of_cores)
    print(f"Key schedule time: {Helper.key_schedule_time}")
    print(f"Encryption time: {Helper.encryption_time}")
if (inp==2):
    image_path = input("Please input image path:")
    key = input("Please input key:")
    no_of_cores = int(input("Please input number of cores:"))
    print("Processing...")
    Helper.decipher(image_path, key, no_of_cores)
    print(f"Key schedule time: {Helper.key_schedule_time}")
    print(f"Encryption time: {Helper.decryption_time}")
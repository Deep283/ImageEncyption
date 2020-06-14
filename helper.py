#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 5:39:54 2020

@author: deepak
"""

from blowfish import Blowfish
import time
import shutil

class Helper:
    blowfish_instance = Blowfish()
    key_schedule_time = 0.000
    encryption_time = 0.000
    decryption_time = 0.000

    @staticmethod
    def initialize_blowfish(key):
        key_array = [ord(x) for x in key]
        start = time.time()
        Helper.blowfish_instance.initialize_blowfish(key_array, len(key_array))
        Helper.key_schedule_time = time.time() - start

    @staticmethod
    def encipher(image_path, key, no_of_cores):
        index = image_path.rindex("/") if "/" in image_path else -1
        image = image_path[index+1:]
        Helper.initialize_blowfish(key)        
        start = time.time()
        Helper.blowfish_instance.encrypt_image(image_path, no_of_cores)
        Helper.encryption_time = time.time() - start
        shutil.move("enciphered_image.jpeg", image_path[:index] + "/enciphered-" + image[:])
        print("Successful, File save in " + image_path[:index])
    
    @staticmethod
    def decipher(image_path, key, no_of_cores):
        index = image_path.rindex("/") if "/" in image_path else -1
        image = image_path[index+1:]
        image = image.replace("enciphered-","") if "enciphered-" in image else image
        Helper.initialize_blowfish(key)        
        start = time.time()
        Helper.blowfish_instance.decrypt_image(image_path,no_of_cores)
        Helper.decryption_time = time.time() - start
        shutil.move("deciphered_image.jpeg", image_path[:index] + "/deciphered-" + image[:])
        print("Successful, File save in " + image_path[:index])


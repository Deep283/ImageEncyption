import BlowfishVariables
import time
import numpy as np
import multiprocessing
import base64
import base64


class Blowfish:
    sbox = BlowfishVariables.sbox
    P = BlowfishVariables.P
    N = 16

    def F(self, x):
        a = [0, 0, 0, 0]

        #dividing into x into 4 8-bits
        # retrieving corresponding values from S-box
        for i in range(0, 4):
            a[i] = x >> (24 - (8 * i))
            a[i] = a[i] & 0xFF
            a[i] = self.sbox[i][a[i]]

        #performing operations of fiestel network
        y = a[0] + a[1]
        y = (y ^ a[2]) + a[3]
        y = y % 0x100000000
        return y

    def initializeBlowfish(self, key, keybytes):
        j = 0
        # an all zero input of 64 bits is divided into 8 bits 
        #and XORed with P array
        for i in range(0, self.N + 2):
            data = 0x00000000
            for k in range(0, 4):
                data = (data << 8) | key[j]
                j = j + 1
                if (j >= keybytes): j = 0
            self.P[i] = self.P[i] ^ data

        # 2 blocks of size 32 bit are taken
        # enciphered and replaced with the values in 
        #P array and S box

        #total iterations = 512
        datal = 0x00000000
        datar = 0x00000000
        for i in range(0, 18, 2):
            data = self.encipher([datal,datar])
            self.P[i] = data[0]
            self.P[i+1] = data[1]

        for i in range(0, 4):
            for j in range(0, 256, 2):
                data = self.encipher(data)
                self.sbox[i][j] = data[0]
                self.sbox[i][j+1] = data[1]

    def encipher(self, x):
        # take left and right blocksofsize 32 bits each
        xl = x[0]
        xr = x[1]
        
        #implementing each round of blowfish algorithm
        for i in range(0, self.N):
            xl = xl ^ self.P[i]
            t = self.F(xl)
            xr = t ^ xr
            t = xl
            xl = xr
            xr = t

        #swap left and right blocks
        t = xl
        xl = xr
        xr = t

        # XOR with 17th and 18th values of P array
        xr = xr ^ self.P[self.N]
        xl = xl ^ self.P[self.N + 1]
        return [xl, xr]

    def decipher(self, x):
        # take left and right 32 bit blocks
        xl = x[0]
        xr = x[1]

        #implementing each round of blowfish algorithm
        for i in range(self.N + 1, 1, -1):
            xl = xl ^ self.P[i]
            t = self.F(xl)
            xr = t ^ xr
            t = xl
            xl = xr
            xr = t

        #swap left and right blocks
        t = xl
        xl = xr
        xr = t

        # XOR with 17th and 18th values of P array
        xr = xr ^ self.P[1]
        xl = xl ^ self.P[0]
        return [xl, xr]

    # takes as input 4 8-bit bytes and converts them into 4 bytes
    def convert32(self, dec8):
        dec32: int = dec8[0]
        for i in range(1, 4):
            dec32 = dec32 << 8
            dec32 = dec32 | dec8[i]
        return dec32    

    # takes as input 32 bit blocks and converts them into 4 8-bit bytes
    def convert8(self, dec32):
        dec8 = [0,0,0,0]
        p = 0
        for i in range(3,-1,-1):
            dec8[i] = dec32 >> p & 255
            p = p+8
        return dec8

    def encrypt_image(self, strImg):
        t= time.time()

        pool = multiprocessing.Pool(processes=15)
        print(multiprocessing.cpu_count())

        str=""
        zeros=[]    


        #read image from specified file and encode in Base64 
        # so that it can be manipulated as bytes
        with open(strImg, "rb") as imageFile:
            str = base64.b64encode(imageFile.read())
        
        #pad zeroes if image is not in multiples of 8 bytes
        #  (blowfish requires 64 bit block as an input)
        if len(str)%8 != 0:
            zeros = [0 for x in range(0,8-(len(str)%8))]
        zeros = bytes(zeros)
        str=str+zeros
        
        #the algorithm requires data as two 32bit blocks
        #  so 4 8-bit blocks are combined together
        inp = [str[x:x+4] for x in range(0,len(str),4)]
        
        #combine into 32 bit block
        result = map(self.convert32,inp)
        result = list(result)
        result = np.array(result)
        
        #reshaping array to an n/8 X 2 array
        result = result.reshape(int(len(result)/2),2)
        
        #create object and initialize blowfish with 8 keys (parameter 1)
        #  and no. of keys (parameter 2)#using multiple threads from the
        #  thread pool to process over the encipher method.
        #  The result array is divided into chunks which it submits
        #  to the process pool as separate tasks.
        result = pool.map_async(self.encipher, result)
        result = np.array(result.get())
        
        #convert array to a one dimensional array
        result = result.reshape(int(len(result)*2))
        
        #divide result in 8 bit chunks
        result = map(self.convert8,result)
        result= list(result)
        inp = []
        
        #create a single list from list of lists
        for x in result:
            inp.extend(x)
        
        #convert list to bytes
        inp = bytes(inp)
        elapsed = time.time() - t
        
        #bytes are written to the image file - Base64 encoded
        fh = open("enciphered_image.jpeg", "wb")
        fh.write(base64.b64encode(inp))
        fh.close()
        return elapsed


    def decrypt_image(self, strImg):
        
        t= time.time()
        pool = multiprocessing.Pool(processes=15)
        print(multiprocessing.cpu_count())

        # convert image to Base64 and store in string str
        str=""


        # read image file and convert to base64
        with open(strImg, "rb") as imageFile:
            str = base64.b64decode(imageFile.read())
        
        # create blocks of 32 bits
        inp = [str[x:x+4] for x in range(0,len(str),4)]
        result = map(self.convert32,inp)
        result = list(result)

        #convert list to np array to reshape
        #  it into n/8 X 2 2-dimensional array
        result = np.array(result)
        result = result.reshape(int(len(result)/2),2)
        
        #using multiple threads from the thread pool to process over 
        # the dencipher method. The result array is divided into chunks 
        # which it submits to the process pool as separate tasks.
        result = pool.map_async(self.decipher, result)
        
        # convert MapResult object into numpy array 
        # so that it can be reshaped into a one dimensional array.
        result = np.array(result.get())
        result = result.reshape(int(len(result)*2))
        
        # dividing the data into blocks on one byte each
        result = map(self.convert8,result)
        result= list(result)
        inp = []
        for x in result:
            inp.extend(x)
        inp = bytes(inp)
        elapsed = time.time() - t
        
        #write all bytes to image file - the data is in base64 
        # encoded bytes which is decoded and written into file.
        fh = open("deciphered_image.jpeg", "wb")
        fh.write(base64.b64decode(inp))
        fh.close()

        return elapsed
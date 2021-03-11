# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 17:02:38 2021

@author: boris
"""

import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("imageName", help="The relative path of the image. The root is where the program is.", type=str)

args = parser.parse_args()
print("The relative path of your image is", args.imageName)


#Name of the image put by the user
filename = args.imageName 

#function which convert little_endian to  big_endian
def to_big(val):
  big_hex = bytearray.fromhex(val)
  big_hex.reverse()
  #print("Byte array format:", big_hex)

  str_big = ''.join(format(x, '02x') for x in big_hex)

  return str_big


#function to open png image
def ouverture_Fichiers_Image_Png(filename):
    f_lecture =open(filename,'rb') #read in binary mode
    i=1
    octet = bytes([0])
    
    
    bitSetT=[]  #variable containing the bit set of the image from the header in binary
    pngT=[]  #variable containing the png format inscription of the image from the header in binary
    crlfT=[]  #variable containing the CRLF Flag the image from the header in binary
    endOfFileT=[]  #variable containing the End of File flag of the image from the header in binary
    lfT=[]  #variable containing the LF Flag of the image from the header in binary
    chunksT=[] #variable containing the chunk (Hlrf,...) of the image from the header in binary
    chunksTS=[] #variable containing the chunks size of the image from the header in binary
    octets=[]
    
    #hex variables
    bitSet=""
    png=""
    crlf=""
    endOfFile=""
    lf=""
    chunks=""
    chunksS=""
    octetPng=[] #variable containing the print of png
    hlrfPng=[]
    size=0
    
    #Lecture du Bit set
    while (i <= 16): #lecture de l'entete: 8 bytes
        octet=f_lecture.read(1) #Lecture octet par octet
        if(i==1):
            bitSetT.append(octet)
            bitSet = bitSet+ " " + octet.hex()
        if(i>=2 and i<=4):
            pngT.append(ord(octet))
            png = png+ " " + octet.hex()
            octetPng.append(octet)
        if(i>=5 and i<=6):
            crlfT.append(octet)
            crlf = crlf+ " " + octet.hex()
        if(i==7):
            endOfFileT.append(octet)
            endOfFile = endOfFile+ " " + octet.hex()
        if(i==8):
            lfT.append(octet)
            lf = lf+ " " + octet.hex()
        if(i>=9 and i<=12):
            chunksTS.append(ord(octet))
            chunksS = chunksS+ " " + octet.hex()
        if(i>=13 and i<=16):
            chunksT.append(ord(octet))
            chunks = chunks+ " " + octet.hex()
            hlrfPng.append(octet)
        i=i+1
    
    
    i=1
    
    #-------------------------------------------------------------------------------------------
    big_endian_set = to_big(bitSet) #variable containing the conversion in big_endian of the bit set of image from the header in binary
    print(bitSet, " =>Bit set =", int(big_endian_set, 16), " octets")
    
    #-------------------------------------------------------------------------------------------
    for x in octetPng: print (x.decode('utf-8')," dec=",ord(x))
    print(png, " =>Format of PNG =", pngT, " P N G => Png")
    
    
    #-------------------------------------------------------------------------------------------
    big_endian_crlf = to_big(crlf) #variable containing the conversion in big_endian CRLF of the image from the header in binary
    print(crlf, " =>CRLF =", int(big_endian_crlf, 16), " octets")
    
    #-------------------------------------------------------------------------------------------
    big_endian_endFile = to_big(endOfFile) #variable containing the conversion in big_endian of the End Of File of the image from the header in binary
    print(endOfFile, " =>End Of File =", int(big_endian_endFile, 16), " octets")
    
    #-------------------------------------------------------------------------------------------
    big_endian_lf = to_big(lf) #variable containing the conversion in big_endian of the LF of the image from the header in binary
    print(lf, " =>LF =", int(big_endian_lf, 16), " octets")
    
    #-------------------------------------------------------------------------------------------
    big_endian_chunksT = to_big(chunksS) #variable containing the conversion in big_endian of the LF of the image from the header in binary
    print(chunksS, " =>Chunks Size =", int(big_endian_chunksT, 16), " octets")
    
    #-------------------------------------------------------------------------------------------Image Header
    for x in hlrfPng: print (x.decode('utf-8')," dec=",ord(x))
    print(chunks, " =>Chunks (Image Header =", chunksT, " octets (4 bytes)")
    
    f_lecture.close

if (args.imageName[-3:]=="png"):
    ouverture_Fichiers_Image_Png(filename)  
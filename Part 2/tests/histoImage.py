# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 23:09:02 2021

@author: boris
"""

import argparse
import os
import sys

#Width of the image
widthImage = 0

#Height of the image
heightImage = 0

#Green pixels global variable for histogram
green=[]

#Blue pixels global variable for histogram
blue=[]

#Red pixels global variable for histogram
red=[]

parser = argparse.ArgumentParser()
parser.add_argument("imageName", help="The relative path of the image. The root is where the program is.", type=str)

parser.add_argument("--histoImage", help="Visualize the histogram of the image.", action="store_true")

args = parser.parse_args()
print("The relative path of your image is", args.imageName)

#Name of the image put by the user
filename = args.imageName 

#Visualisation: on importe matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#function which convert little_endian to  big_endian
def to_big(val):
  big_hex = bytearray.fromhex(val)
  big_hex.reverse()
  #print("Byte array format:", big_hex)

  str_big = ''.join(format(x, '02x') for x in big_hex)

  return str_big

def histo_visualize(filename):
    #Visualisation de l'histogramme de l'image
    img = mpimg.imread(filename)
    plt.hist(red, color='red', bins=256, alpha=0.5, label='red') #calculating histogram
    plt.hist(green, color='green', bins=256, alpha=0.5, label='green') #calculating histogram
    plt.hist(blue, color='blue', bins=256, alpha=0.5, label='blue') #calculating histogram
    plt.legend(loc='upper right')
    plt.show()
    

#function to open bmp image
def ouverture_Fichiers_Image(filename):
    f_lecture =open(filename,'rb') #read in binary mode
    i=1
    octet = bytes([0])
    
    
    octets=[]
    octets_size=[] #variable containing the size of the image from the header in binary
    octets_app=[] #variable containing the application name from the header in binary
    octets_size_header=[] #variable containing the size of the image's header from the header in binary
    octets_size_width=[] #variable containing the width size of the image from the header in binary
    octets_size_height=[] #variable containing the height size of the image from the header in binary
    octets_planes=[] #variable containing the number of planes of the picture
    octets_colours=[] #variable containing the number of color of the picture   
    
    size=0
    
    #Lecture du MAGIC NUMBER
    while (i <=2): #lecture Magic number sur 2 octets
        octet=f_lecture.read(1) #Lecture octet par octet
        octets.append(ord(octet))
        print (octet.decode('utf-8')," dec=",ord(octet))
        i=i+1
    print(" =>Magic Number =", octets, " BM => BitMap")
    
    i=1
    
    #hex variables
    hexDecSiz=[]
    hexStrSiz=""
    hexStrApp=""
    hexStrSizHeader=""
    hexStrSizWidth=""
    hexStrSizHeight=""
    hexStrPlanes=""
    hexStrColours=""
    
    
    #BLOC ENTETE 54 octets en standard
    while (i<=54):
        octet=f_lecture.read(1)
        if (i>=1 and i<=4): #size of the file in octets
            octets_size.append(octet)
            #print (octet.hex()) #print the hex
            hexStrSiz = hexStrSiz + " " + octet.hex()  
        if (i>=5 and i<=8): #application image
            octets_app.append(octet)
            hexStrApp = hexStrApp + " " + octet.hex()  
        if (i>=9 and i<=12): #print size of the file's header
            octets_size_header.append(octet)
            hexStrSizHeader = hexStrSizHeader+ " " + octet.hex()  
        if (i>=17 and i<=20): #print size of the picture's width
            octets_size_width.append(octet)
            hexStrSizWidth = hexStrSizWidth+ " " + octet.hex()
        if (i>=21 and i<=24): #print size of the picture's height
            octets_size_height.append(octet)
            hexStrSizHeight = hexStrSizHeight+ " " + octet.hex()
        if (i>=25 and i<=26): #print number of planes in the image
            octets_planes.append(octet)
            hexStrPlanes = hexStrPlanes+ " " + octet.hex()
        if (i>=27 and i<=28): #print number of colours in the image
            octets_colours.append(octet)
            hexStrColours = hexStrColours+ " " + octet.hex()
            
        i=i+1
    big_endian_siz = to_big(hexStrSiz)
    #print("Big endian hex:", big_endian_siz)
    #print("Hex to int:", int(big_endian_siz, 16))
    print(hexStrSiz, " =>Taille de fichier =", int(big_endian_siz, 16), " octets")
    
    hexStrSiz = hexStrSiz.replace(" ", "") # we remove all spaces
    for m in range(0, len(hexStrSiz), 2): # we take the characters two by two
        code = hexStrSiz[m:m+2]
        hexDecSiz.append(int(code, 16)) # we convert in decimal and we put in the list hexDecSiz
    print(hexDecSiz, " =>Taille de fichier =", int(big_endian_siz, 16), " octets")
    
    #-------------------------------------------------------------------------------------------
    big_endian_app = to_big(hexStrApp) #variable containing the conversion in big_endian of the application of image from the header in binary
    print(hexStrApp, " =>application image =", int(big_endian_app, 16), " noms")
    
    #-------------------------------------------------------------------------------------------
    big_endian_size_header = to_big(hexStrSizHeader) #variable containing the conversion in big_endian of the size of the image from the header in binary
    print(hexStrSizHeader, " =>Taille Entete =", int(big_endian_size_header, 16), " octets")
    
    #-------------------------------------------------------------------------------------------
    big_endian_size_width = to_big(hexStrSizWidth) #variable containing the conversion in big_endian of the width size of the image from the header in binary
    print(hexStrSizWidth, " =>Largeur Image =", int(big_endian_size_width, 16), " pixels")
    
    #-------------------------------------------------------------------------------------------
    big_endian_size_height = to_big(hexStrSizHeight) #variable containing the conversion in big_endian of the height size of the image from the header in binary
    print(hexStrSizHeight, " =>Hauteur Image =", int(big_endian_size_height, 16), " pixels")
    
    #-------------------------------------------------------------------------------------------
    big_endian_planes = to_big(hexStrPlanes) #variable containing the conversion in big_endian of the number of planes of the image from the header in binary
    print(hexStrPlanes, " =>NB plan Image =", int(big_endian_planes, 16), " plan")
    
    #-------------------------------------------------------------------------------------------
    big_endian_colours = to_big(hexStrColours) #variable containing the conversion in big_endian of the number of colour image from the header in binary
    print(hexStrColours, " =>NB Couleur Image =", int(big_endian_colours, 16), " couleurs")
    
    global widthImage 
    global heightImage
    global green
    global red
    global blue
    
    widthImage = int(big_endian_size_width, 16)
    heightImage = int(big_endian_size_height, 16)
    
    
    trioctets=[]
    octetsHex=""
    i=1
    pixel_end = widthImage*heightImage*3+1
    f_lecture.seek(54)
    #Lecture of the pixels of the image
    while (i< pixel_end): #lecture Magic number sur 2 octets
        octet=f_lecture.read(1) #Lecture octet par octet
        octetsHex = octetsHex+ " " + octet.hex() 
        big_endian_octet = to_big(octetsHex)
        octetDec = int(big_endian_octet, 16)
       
        trioctets.append(octetDec)
        i = i+1
        octetsHex=""
    
    for i in range(0, len(trioctets), 3):
        blue.append(trioctets[i])
        green.append(trioctets[i+1])
        red.append(trioctets[i+2])
        
    f_lecture.close


#-------------ouverture_Fichiers_Image 
if (args.imageName[-3:] == "bmp"):
    sizeImage = ouverture_Fichiers_Image(filename)  
    
#-------------histoImage 
if (args.histoImage and args.imageName[-3:] == "bmp"):
    histo_visualize(args.imageName)  

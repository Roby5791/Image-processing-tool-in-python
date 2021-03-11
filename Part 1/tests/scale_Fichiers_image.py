# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 16:18:10 2021

@author: boris
"""

#Visualisation: on importe matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
    
import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("imageName", help="The relative path of the image. The root is where the program is.", type=str)

#----------------------------------------Arguments optionnels--------------------------------------
parser.add_argument("--scaleFactor", help="Enter the scale factor of your image color. NB: This value must be between 1 and 10 ! Ex: 1")

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

def visualize(filename):
    #Visualisation d’une image avec Matplotlib 
    img = mpimg.imread(filename)
    imgplot = plt.imshow(img)
    plt.show()

#function which scales the image
def scale_image(scale, filename):
    
    octets_size=[] #variable containing each octet of the picture (we will append after when we will look for the RGB in a for loop of a given number of pixel)
    octets_size_width=[] #variable containing the width size of the image from the header in binary
    octets_size_height=[] #variable containing the height size of the image from the header in binary  

    hexStrSizWidth="" #variable containing the width size of the image from the header in binary in hex
    hexStrSizHeight="" #variable containing the height size of the image from the header in binary in hex
    big_endian_size_width=0 #variable containing the conversion in big_endian of the width size of the image from the header in binary
    big_endian_size_height=0 #variable containing the conversion in big_endian of the height size of the image from the header in binary
    f_lecture =open(filename,'rb') #read in binary mode
    outputName = "scale_" + filename
    f_ecriture =open(outputName, 'wb') #read in binary mode
    octet = bytes([0])
    
    entete_image=[]
   
    i=1
    while (i <= 54):
        octet=f_lecture.read(1) #Lecture octet par octet
        if (i>=19 and i<=22): #print size of the picture's width
            octets_size_width.append(octet)
            hexStrSizWidth = hexStrSizWidth+ " " + octet.hex() # we convert in hex with octet.hex
            big_endian_size_width = to_big(hexStrSizWidth) #we convert to big endian
        if (i>=23 and i<=26): #print size of the picture's height
            octets_size_height.append(octet)
            hexStrSizHeight = hexStrSizHeight+ " " + octet.hex()
            big_endian_size_height = to_big(hexStrSizHeight)
            
            octets_size.append(octet)
        entete_image.append(octet)
            
        i=i+1
    print(big_endian_size_height, " =>Largeur Image =", int(big_endian_size_width, 16), " pixels")
    print(big_endian_size_height, " =>Hauteur Image =", int(big_endian_size_height, 16), " pixels")
    i=1
    
    hexSizWidth=int(big_endian_size_width, 16)
    hexSizHeight=int(big_endian_size_height, 16)
    
    pixel_end = (int(big_endian_size_height,16)*int(big_endian_size_width,16))
    
        
    octets_s=[]
    octets_s_r=[]
    scale_list=[]
    
    for i in range (hexSizWidth):
        for j in range(hexSizHeight):
            octets_s_r.append(f_lecture.read(3))
        octets_s.append(octets_s_r)
        octets_s_r = []
    
    for x in entete_image:
        f_ecriture.write(x)
   
    if(scale>0):
        for i in range(hexSizWidth):
            for j in range(hexSizHeight):
                for k in range(scale):
                    octets_s_r.append(octets_s[i][j])
                    #f_ecriture.write(octets_s[i][j])
            for l in range(scale):
                scale_list.append(octets_s_r)
            octets_s_r=[]
    else:
        print("The scale you enter must be positive !")
           
    for i in range(hexSizWidth*scale):
        temp = scale_list[i]
        for j in temp:
            f_ecriture.write(j)
     
    f_lecture.close()
    f_ecriture.close()
    
    #print(octets_s_r)
    #print(len(octets_s_r))
  
#-----------scale_Fichiers_image----------
if (args.scaleFactor and int(args.scaleFactor) >= 1 and int(args.scaleFactor) <= 10):
    print("\n The factor of scale you want to do is", args.scaleFactor)
    scale_image(int(args.scaleFactor), filename)
    outputName = "scale_" + filename
    visualize(outputName)
elif(args.scaleFactor):
    print("\n Error: The parameter scaleFactor must be between 1 and 10 !")

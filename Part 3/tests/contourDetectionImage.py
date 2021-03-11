# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 00:24:25 2021

@author: boris
"""


import argparse
import os
import sys

import numpy as np
np.set_printoptions(threshold=sys.maxsize)

#Visualisation: on importe matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

parser = argparse.ArgumentParser()
parser.add_argument("imageName", help="The relative path of the image. The root is where the program is.", type=str)

parser.add_argument("--contourDetection", help="Enter the output name of your image color for contour detection. Ex: contour_lena_couleur.bmp")

args = parser.parse_args()
print("The relative path of your image is", args.imageName)

#Name of the image put by the user
filename = args.imageName 

#def contourDetectionImage(filename):
def visualize(filename):
    #Visualisation d’une image avec Matplotlib 
    img = mpimg.imread(filename)
    imgplot = plt.imshow(img)
    plt.show()

#function which convert little_endian to  big_endian
def to_big(val):
  big_hex = bytearray.fromhex(val)
  big_hex.reverse()
  #print("Byte array format:", big_hex)

  str_big = ''.join(format(x, '02x') for x in big_hex)

  return str_big

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
    
    widthImage = int(big_endian_size_width, 16)
    heightImage = int(big_endian_size_height, 16)
        
    f_lecture.close

#Function for convolution
def convolve(image, kernel):
  
    if(image.ndim == 2):
        image = image[:, :, None]
        
    if(kernel.ndim == 2):
        kernel = np.repeat(np.expand_dims(kernel, axis=-1), image.shape[-1], axis=-1)
        
    if(kernel.shape[-1] == 1):
        kernel = np.repeat(kernel, image.shape[-1], axis=-1) 
    
    assert image.shape[-1] == kernel.shape[-1]
    
    xk = kernel.shape[0]
    yk = kernel.shape[0]
   
    width, height = image.shape[:2]

    # Convolution Output: [(W−K+2P)/S]+1
    output_array = np.zeros(((width - xk + 2) + 1, (height - yk + 2) + 1, image.shape[-1])) 
    
    padded_image = np.pad(image, [(1, 1), (1, 1), (0, 0)])
    
    for x in range(padded_image.shape[0] - xk + 1): # -xk + 1 is to keep the window within the bounds of the image
        for y in range(padded_image.shape[1] - yk + 1):

            # Creates the window with the same size as the filter
            window = padded_image[x:x + xk, y:y + yk]

            # Sums over the product of the filter and the window
            output_values = np.sum(kernel * window, axis=(0, 1)) 

            # Places the calculated value into the output_array
            output_array[x, y] = output_values
            
    return output_array

#function for contour detection (filter)
def contourDetection(filename):
    f_lecture =open(filename,'rb') #read in binary mode
    f_ecriture =open(args.contourDetection,'wb') #read in binary mode
    
    i=1
    octet = bytes([0])
    
    trioctets=[]
    
    #hex variables
    octetsHex=""
    
    #Lecture du MAGIC NUMBER
    while (i <=2): #lecture Magic number sur 2 octets
        octet=f_lecture.read(1) #Lecture octet par octet
        f_ecriture.write(octet)
        i=i+1
    
    i=1
    
    #Lecture du MAGIC NUMBER
    while (i<= 54): #lecture Magic number sur 2 octets
        octet=f_lecture.read(1) #Lecture octet par octet
        f_ecriture.write(octet)
       
        i = i+1
    
    i=1
    f_lecture.seek(54)
    f_ecriture.seek(54)
    pixel_end = widthImage*heightImage*3+1
    #Lecture of the pixels of the image
    while (i< pixel_end): #lecture Magic number sur 2 octets
        octet=f_lecture.read(1) #Lecture octet par octet
        octetsHex = octetsHex+ " " + octet.hex() 
        big_endian_octet = to_big(octetsHex)
        octetDec = int(big_endian_octet, 16)
        trioctets.append(octetDec)
        i = i+1
        octetsHex=""
    
    trioctets = np.array(trioctets)
    tri = trioctets.reshape((widthImage,heightImage,3))
    kernel =  [[  0  , 1 ,   0],
              [  1 ,   -4 ,  1 ],
              [  0  , 1 ,    0 ]]
    kernel = np.array(kernel)

    convolution = convolve(tri, kernel)

    for i in convolution:
        for j in i: 
            for k in j:
                if (k <0): 
                    k = 0
                if (k > 255): 
                    k = 255
                f_ecriture.write(int(k).to_bytes(1,'little'))

#-------------ouverture_Fichiers_Image 
if (args.imageName[-3:] == "bmp"):
    sizeImage = ouverture_Fichiers_Image(filename)  

#-------------contourDetection
if (args.contourDetection and args.contourDetection[-3:] == "bmp"):
    contourDetection(filename) 
    print("The size of your image ", args.imageName, " is ", widthImage, " * ", heightImage, " .")
    visualize(args.contourDetection)



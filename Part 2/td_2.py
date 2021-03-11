# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 23:03:51 2021

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

#----------------------------------------Arguments optionnels--------------------------------------
parser.add_argument("--copyImage", help="Enter the output name of your image color. Ex: copy_lena_couleur.bmp")
parser.add_argument("--contrastImage", help="Enter the level contrast of your image color. NB: This value must be between -255 and 255 ! Ex: 100")
parser.add_argument("--grayImage", help="Enter the output name of your image color for gray image. Ex: gray_lena_couleur.bmp")
parser.add_argument("--blackWhiteImage", help="Enter the output name of your image color for black and white image. Ex: bw_lena_couleur.bmp")
parser.add_argument("--negativeImage", help="Enter the output name of your image color for negative image. Ex: negative_lena_couleur.bmp")
parser.add_argument("--redOnlyImage", help="Enter the output name of your image color for red only image. Ex: redOnly_lena_couleur.bmp")
parser.add_argument("--greenOnlyImage", help="Enter the output name of your image color for green only image. Ex: greenOnly_lena_couleur.bmp")
parser.add_argument("--blueOnlyImage", help="Enter the output name of your image color for blue only image. Ex: blueOnly_lena_couleur.bmp")
parser.add_argument('--twoColorsImage', nargs='+', help="Enter the two colors and their position you want to build your image color with. NB: The colors must be between 0 and 255 and the positions between 0 and 2 ! : 0 for Blue, 1 for Green, 2 for Red. Ex: 100 100 0 1. \n NB: You can't enter one or three parameters")

parser.add_argument("--histoImage", help="Visualize the histogram of the image.", action="store_true")
#parser.add_argument("--rotateDegree", help="Enter the degree of rotation of your image color. NB: This value must be 90, 180 or 270 ! Ex: 90")
#parser.add_argument("--scaleFactor", help="Enter the scale factor of your image color. NB: This value must be between 1 and 10 ! Ex: 1")

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

def visualize(filename):
    #Visualisation d’une image avec Matplotlib 
    img = mpimg.imread(filename)
    imgplot = plt.imshow(img)
    plt.show()

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

def copyImage(filename):
    f_lecture =open(filename,'rb') #read in binary mode
    f_ecriture =open(args.copyImage,'wb') #read in binary mode
    octet = bytes([0])
    
    
    octets=[]
    
    i=1
    #Lecture du MAGIC NUMBER
    while (i <=2): #lecture Magic number sur 2 octets
        octet=f_lecture.read(1) #Lecture octet par octet
        f_ecriture.write(octet)
        i=i+1
    print(" =>Magic Number =", octets, " BM => BitMap")
    
    i=1
    
    #Lecture du MAGIC NUMBER
    while (i<= 54): #lecture Magic number sur 2 octets
        octet=f_lecture.read(1) #Lecture octet par octet
        f_ecriture.write(octet)
        i = i+1
    
    #print(f_ecriture.tell())
    i=1
    f_lecture.seek(54)
    f_ecriture.seek(54)
    pixel_end = widthImage*heightImage*3+1
    #Lecture of the pixels of the image
    while (i< pixel_end): #lecture Magic number sur 2 octets
        octet=f_lecture.read(1) #Lecture octet par octet
        f_ecriture.write(octet)        
        i = i+1
        
    f_lecture.close

#function to modify the contrast
def modifyContrast(factor, color):
    return (factor*(color - 128) + 128)

#We readjuste the value of the contrast
def readjust(value):
    if (value < 0):
        return 0
    elif (value > 255):
        return 255
    else:
        return value

#function to modify the contrast
def contrast_image(contrast, filename):
    
    f_lecture =open(filename,'rb') #read in binary mode
    outputName = "contrast_" + filename
    f_ecriture =open(outputName,'wb') #read in binary mode
    i=1
    octet = bytes([0])   
    octets=[]
  
    #hex variables
    octetsHex=""
    
    factor = (259*(int(contrast)+255)) / (255*(259 - int(contrast)))
    #print("factor", factor)
    
    #Lecture du MAGIC NUMBER
    while (i <=2): #lecture Magic number sur 2 octets
    
        octet=f_lecture.read(1) #Lecture octet par octet
        f_ecriture.write(octet)
    
        i=i+1
    print(" =>Magic Number =", octets, " BM => BitMap")
    i=1
    #Lecture du MAGIC NUMBER
    while (i<= 54): #lecture Magic number sur 2 octets
        octet=f_lecture.read(1) #Lecture octet par octet
        f_ecriture.write(octet)
        i = i+1
    
    #print(f_ecriture.tell())
    i=1
    pixel_end = widthImage*heightImage*3+1
    f_lecture.seek(54)
    f_ecriture.seek(54)
    #Lecture of the pixels of the image
    while (i< pixel_end): #lecture Magic number sur 2 octets
        octet=f_lecture.read(1) #Lecture octet par octet
        octetsHex = octetsHex+ " " + octet.hex() 
        big_endian_octet = to_big(octetsHex)
        octetDec = int(big_endian_octet, 16)
      
        f_ecriture.write(int(readjust(modifyContrast(factor, octetDec))).to_bytes(1, 'little'))       
        i = i+1
        octetsHex=""
        
    f_lecture.close
  
#function to transform in shades gray
def gray_image(filename):
   
    f_lecture =open(filename,'rb') #read in binary mode
    f_ecriture =open(args.grayImage,'wb') #read in binary mode
    i=1
    octet = bytes([0])
     
    #hex variables
    octetsHex=""
    trioctets=[]

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
    
    #print(f_ecriture.tell())
    i=1
    pixel_end = widthImage*heightImage*3+1
    f_lecture.seek(54)
    f_ecriture.seek(54)
    #Lecture of the pixels of the image
    while (i< pixel_end): #lecture Magic number sur 2 octets
        octet=f_lecture.read(1) #Lecture octet par octet
        octetsHex = octetsHex+ " " + octet.hex() 
        big_endian_octet = to_big(octetsHex)
        octetDec = int(big_endian_octet, 16)
      
        trioctets.append(octetDec)
        i = i+1
        octetsHex=""
    temp=0

    for i in range(0, len(trioctets), 3):
        for j in range (0+i,3+i):
            
            temp = temp + trioctets[j]
        temp = temp/3
        #if (i==0):
            #print(temp)
        f_ecriture.write(int(temp).to_bytes(1, 'little'))  
        f_ecriture.write(int(temp).to_bytes(1, 'little')) 
        f_ecriture.write(int(temp).to_bytes(1, 'little')) 
        temp = 0
    f_lecture.close



#function to transform image in black and white only
def blackWhite_image(filename):
   
    f_lecture =open(filename,'rb') #read in binary mode
    f_ecriture =open(args.blackWhiteImage,'wb') #read in binary mode
    i=1
    octet = bytes([0])
     
    octets=[]
    
    #hex variables
    octetsHex=""
    trioctets=[]

    #Lecture du MAGIC NUMBER
    while (i <=2): #lecture Magic number sur 2 octets
    
        octet=f_lecture.read(1) #Lecture octet par octet
        f_ecriture.write(octet)
        octets.append(ord(octet))
        print (octet.decode('utf-8')," dec=",ord(octet))
    
        i=i+1
    print(" =>Magic Number =", octets, " BM => BitMap")
    i=1
    #Lecture du MAGIC NUMBER
    while (i<= 54): #lecture Magic number sur 2 octets
        octet=f_lecture.read(1) #Lecture octet par octet
        f_ecriture.write(octet)   
        i = i+1
    
    #print(f_ecriture.tell())
    i=1
    pixel_end = widthImage*heightImage*3+1
    f_lecture.seek(54)
    f_ecriture.seek(54)
    #Lecture of the pixels of the image
    while (i< pixel_end): #lecture Magic number sur 2 octets
        octet=f_lecture.read(1) #Lecture octet par octet
        octetsHex = octetsHex+ " " + octet.hex() 
        big_endian_octet = to_big(octetsHex)
        octetDec = int(big_endian_octet, 16)
        
        trioctets.append(octetDec)
        i = i+1
        octetsHex=""
    temp=0

    for i in range(0, len(trioctets), 3):
        for j in range (0+i,3+i):
            
            temp = temp + trioctets[j]
        temp = temp/3
        
        if(temp < 128):
            temp = 0
        else:
            temp = 255
        
        #if (i==0):
            #print(temp)
        f_ecriture.write(int(temp).to_bytes(1, 'little'))  
        f_ecriture.write(int(temp).to_bytes(1, 'little')) 
        f_ecriture.write(int(temp).to_bytes(1, 'little')) 
        temp = 0
            
        
    f_lecture.close
    
#function to transform image in negative
def negative_image(filename):
   
    f_lecture =open(filename,'rb') #read in binary mode
    f_ecriture =open(args.negativeImage,'wb') #read in binary mode
    i=1
    octet = bytes([0])
     
    octets=[]
  
    #hex variables
    octetsHex=""
    trioctets=[]

    #Lecture du MAGIC NUMBER
    while (i <=2): #lecture Magic number sur 2 octets
        octet=f_lecture.read(1) #Lecture octet par octet
        f_ecriture.write(octet)
        i=i+1
    print(" =>Magic Number =", octets, " BM => BitMap")
    i=1
    #Lecture du MAGIC NUMBER
    while (i<= 54): #lecture Magic number sur 2 octets
        octet=f_lecture.read(1) #Lecture octet par octet
        f_ecriture.write(octet) 
        i = i+1
    
    #print(f_ecriture.tell())
    i=1
    pixel_end = widthImage*heightImage*3+1
    f_lecture.seek(54)
    f_ecriture.seek(54)
    #Lecture of the pixels of the image
    while (i< pixel_end): #lecture Magic number sur 2 octets
        octet=f_lecture.read(1) #Lecture octet par octet
        octetsHex = octetsHex+ " " + octet.hex() 
        big_endian_octet = to_big(octetsHex)
        octetDec = int(big_endian_octet, 16)
        
        trioctets.append(octetDec)
        i = i+1
        octetsHex=""
    temp=0
   
    for i in range(0, len(trioctets)):
        temp = trioctets[i]
        temp = 255 - temp
        f_ecriture.write(int(temp).to_bytes(1, 'little'))  
       
        temp = 0
    f_lecture.close
    
#function to print image in red only
def redOnly_image(filename):
   
    f_lecture =open(filename,'rb') #read in binary mode
    f_ecriture =open(args.redOnlyImage,'wb') #read in binary mode
    i=1
    octet = bytes([0])
     
    octets=[]
    
    #hex variables
    octetsHex=""
    trioctets=[]

    #Lecture du MAGIC NUMBER
    while (i <=2): #lecture Magic number sur 2 octets
    
        octet=f_lecture.read(1) #Lecture octet par octet
        f_ecriture.write(octet)
        octets.append(ord(octet))
        print (octet.decode('utf-8')," dec=",ord(octet))
    
        i=i+1
    print(" =>Magic Number =", octets, " BM => BitMap")
    i=1
    #Lecture du MAGIC NUMBER
    while (i<= 54): #lecture Magic number sur 2 octets
        octet=f_lecture.read(1) #Lecture octet par octet
        f_ecriture.write(octet)   
        i = i+1
    
    #print(f_ecriture.tell())
    i=1
    pixel_end = widthImage*heightImage*3+1
    f_lecture.seek(54)
    f_ecriture.seek(54)
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
        trioctets[i] = 0
        trioctets[i+1] = 0
        
        f_ecriture.write(int(trioctets[i]).to_bytes(1, 'little'))  
        f_ecriture.write(int(trioctets[i+1]).to_bytes(1, 'little')) 
        f_ecriture.write(int(trioctets[i+2]).to_bytes(1, 'little')) 
            
        
    f_lecture.close
    
#function to print image in green only
def greenOnly_image(filename):
   
    f_lecture =open(filename,'rb') #read in binary mode
    f_ecriture =open(args.greenOnlyImage,'wb') #read in binary mode
    i=1
    octet = bytes([0])
     
    octets=[]
    
    #hex variables
    octetsHex=""
    trioctets=[]

    #Lecture du MAGIC NUMBER
    while (i <=2): #lecture Magic number sur 2 octets
    
        octet=f_lecture.read(1) #Lecture octet par octet
        f_ecriture.write(octet)
        octets.append(ord(octet))
        print (octet.decode('utf-8')," dec=",ord(octet))
    
        i=i+1
    print(" =>Magic Number =", octets, " BM => BitMap")
    i=1
    #Lecture du MAGIC NUMBER
    while (i<= 54): #lecture Magic number sur 2 octets
        octet=f_lecture.read(1) #Lecture octet par octet
        f_ecriture.write(octet)
        i = i+1
    
    #print(f_ecriture.tell())
    i=1
    pixel_end = widthImage*heightImage*3+1
    f_lecture.seek(54)
    f_ecriture.seek(54)
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
        trioctets[i] = 0
        trioctets[i+2] = 0
        
        f_ecriture.write(int(trioctets[i]).to_bytes(1, 'little'))  
        f_ecriture.write(int(trioctets[i+1]).to_bytes(1, 'little')) 
        f_ecriture.write(int(trioctets[i+2]).to_bytes(1, 'little')) 
            
        
    f_lecture.close
    

#function to print image in blue only
def blueOnly_image(filename):
   
    f_lecture =open(filename,'rb') #read in binary mode
    f_ecriture =open(args.blueOnlyImage,'wb') #read in binary mode
    i=1
    octet = bytes([0])
     
    octets=[]
    
    #hex variables
    octetsHex=""
    trioctets=[]

    #Lecture du MAGIC NUMBER
    while (i <=2): #lecture Magic number sur 2 octets
    
        octet=f_lecture.read(1) #Lecture octet par octet
        f_ecriture.write(octet)
        octets.append(ord(octet))
        print (octet.decode('utf-8')," dec=",ord(octet))
    
        i=i+1
    print(" =>Magic Number =", octets, " BM => BitMap")
    i=1
    #Lecture du MAGIC NUMBER
    while (i<= 54): #lecture Magic number sur 2 octets
        octet=f_lecture.read(1) #Lecture octet par octet
        f_ecriture.write(octet)
        i = i+1
    
    #print(f_ecriture.tell())
    i=1
    pixel_end = widthImage*heightImage*3+1
    f_lecture.seek(54)
    f_ecriture.seek(54)
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
        trioctets[i+1] = 0
        trioctets[i+2] = 0
        
        f_ecriture.write(int(trioctets[i]).to_bytes(1, 'little'))  
        f_ecriture.write(int(trioctets[i+1]).to_bytes(1, 'little')) 
        f_ecriture.write(int(trioctets[i+2]).to_bytes(1, 'little')) 
            
        
    f_lecture.close
    
#function to print image only in two primary colors
def twoColors_image(filename, color1, color2, pos1, pos2):
   
    f_lecture =open(filename,'rb') #read in binary mode
    outputName = "twoColors_" + filename
    f_ecriture =open(outputName,'wb') #read in binary mode
    i=1
    octet = bytes([0])
     
    octets=[]
    
    #hex variables
    octetsHex=""
    trioctets=[]

    #Lecture du MAGIC NUMBER
    while (i <=2): #lecture Magic number sur 2 octets
    
        octet=f_lecture.read(1) #Lecture octet par octet
        f_ecriture.write(octet)
        i=i+1
    print(" =>Magic Number =", octets, " BM => BitMap")
    i=1
    #Lecture du MAGIC NUMBER
    while (i<= 54): #lecture Magic number sur 2 octets
        octet=f_lecture.read(1) #Lecture octet par octet
        f_ecriture.write(octet)    
        i = i+1
    
    #print(f_ecriture.tell())
    i=1
    pixel_end = widthImage*heightImage*3+1
    f_lecture.seek(54)
    f_ecriture.seek(54)
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
        #trioctets[i] = 0
        trioctets[i+pos1] = color1
        trioctets[i+pos2] = color2
        
        f_ecriture.write(int(trioctets[i]).to_bytes(1, 'little'))  
        f_ecriture.write(int(trioctets[i+1]).to_bytes(1, 'little')) 
        f_ecriture.write(int(trioctets[i+2]).to_bytes(1, 'little')) 
            
        
    f_lecture.close
    
#-------------ouverture_Fichiers_Image 
if (args.imageName[-3:] == "bmp"):
    sizeImage = ouverture_Fichiers_Image(filename)  
    
#-------------copyImage
if (args.copyImage and args.copyImage[-3:] == "bmp"):
    copyImage(filename) 
    print("The size of your image ", args.imageName, " is ", widthImage, " * ", heightImage, " .")
    visualize(args.copyImage)

#-----------contrastImage
if (args.contrastImage and int(args.contrastImage) >= -255 and int(args.contrastImage) <= 255):
    print("\n The contrast you want to apply to the color image is: ", args.contrastImage)
    contrast_image(int(args.contrastImage), filename)
    outputName = "contrast_" + filename
    visualize(outputName)
#The value of contrast will be between -255 and +255
elif (args.contrastImage and int(args.contrastImage) < -255 and int(args.contrastImage) > 255):
    print("The value of the contrast must be between -255 and 255")
elif(args.contrastImage):
    print("\n Error: The parameter contrastImage must be between -255 and 255 !")
    
#-------------shadesGrayImage
if (args.grayImage and args.grayImage[-3:] == "bmp"):
    gray_image(filename) 
    visualize(args.grayImage)
    
#-------------BlackWhiteImage
if (args.blackWhiteImage and args.blackWhiteImage[-3:] == "bmp"):
    blackWhite_image(filename) 
    visualize(args.blackWhiteImage)

#-------------NegativeImage
if (args.negativeImage and args.negativeImage[-3:] == "bmp"):
    negative_image(filename) 
    visualize(args.negativeImage)
    
#-------------redOnlyImage
if (args.redOnlyImage and args.redOnlyImage[-3:] == "bmp"):
    redOnly_image(filename) 
    visualize(args.redOnlyImage)
    
#-------------greenOnlyImage
if (args.greenOnlyImage and args.greenOnlyImage[-3:] == "bmp"):
    greenOnly_image(filename) 
    visualize(args.greenOnlyImage)
    
#-------------blueOnlyImage
if (args.blueOnlyImage and args.blueOnlyImage[-3:] == "bmp"):
    blueOnly_image(filename) 
    visualize(args.blueOnlyImage)
    
#-------------twoColorsImage
if (args.twoColorsImage and len(args.twoColorsImage) == 4 and args.twoColorsImage[0] and args.twoColorsImage[1] and int(args.twoColorsImage[0]) >= 0 and int(args.twoColorsImage[0]) <= 255 and int(args.twoColorsImage[1]) >= 0 and int(args.twoColorsImage[1]) <= 255 and int(args.twoColorsImage[2]) >= 0 and int(args.twoColorsImage[2]) <= 2 and int(args.twoColorsImage[3]) >= 0 and int(args.twoColorsImage[3]) <= 2 ):    
    print("\n The values of the two colors you want to apply to the color image are: ", int(args.twoColorsImage[0]), int(args.twoColorsImage[1]), "and the position are: ", int(args.twoColorsImage[2]), int(args.twoColorsImage[3]))
    twoColors_image(filename, int(args.twoColorsImage[0]), int(args.twoColorsImage[1]), int(args.twoColorsImage[2]), int(args.twoColorsImage[3])) 
    outputName = "twoColors_" + filename
    visualize(outputName)

elif (args.twoColorsImage and len(args.twoColorsImage) == 4 and args.twoColorsImage[0] and args.twoColorsImage[1] and (int(args.twoColorsImage[0]) < 0 or int(args.twoColorsImage[0]) > 255 or int(args.twoColorsImage[1]) < 0 or int(args.twoColorsImage[1]) > 255 or int(args.twoColorsImage[2]) < 0 or int(args.twoColorsImage[2]) > 2 or int(args.twoColorsImage[3]) < 0 or int(args.twoColorsImage[3]) > 2 )):
    print("\n Error: The parameters twoColorsImage of the two colors must be between 0 and 255 !")  
    print("\n Error: The two last parameters twoColorsImage of the two colors must be between 0 and 2 !")

elif(args.twoColorsImage and (len(args.twoColorsImage) == 1 or len(args.twoColorsImage) == 2 or len(args.twoColorsImage) == 3)):
    print("\n Error: You must enter four parameters !")
    
#-------------histoImage 
if (args.histoImage and args.imageName[-3:] == "bmp"):
    histo_visualize(args.imageName)  

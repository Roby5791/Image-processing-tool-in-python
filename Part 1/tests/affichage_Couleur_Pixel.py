# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 09:53:47 2021
This script print the RGB of a pixel with the function colour_pixel. 

The parameters are the number of the pixel (Between 1 and PixelWidthImage*PixelHeightImage) 
And the Name of the picture


@author: boris
"""
import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("imageName", help="The relative path of the image. The root is where the program is.", type=str)

#----------------------------------------Arguments optionnels--------------------------------------

parser.add_argument("--colorPixel", help="Enter the color pixel of your image color. Ex: For a 515x512 color image, you can put 262144. NB: 0 <= colorPixel <= widthImage*heightImage")

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

#function which convert little_endian to  big_endian
def colour_pixel(pixel_num, filename):
    octets_size=[] #variable containing each octet of the picture (we will append after when we will look for the RGB in a for loop of a given number of pixel)

    octets_size_width=[] #variable containing the width size of the image from the header in binary
    octets_size_height=[] #variable containing the height size of the image from the header in binary  
    
    hexStrPix="" #variable containing the RGB of the pixel nb_pixel in hex
    
    hexStrSizWidth="" #variable containing the width size of the image from the header in binary in hex
    hexStrSizHeight="" #variable containing the height size of the image from the header in binary in hex
    big_endian_size_width=0 #variable containing the conversion in big_endian of the width size of the image from the header in binary
    big_endian_size_height=0 #variable containing the conversion in big_endian of the height size of the image from the header in binary
    f_lecture =open(filename,'rb') #read in binary mode
    octet = bytes([0])
   
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
            
        i=i+1
    print(hexStrSizWidth, " =>Largeur Image =", int(big_endian_size_width, 16), " pixels")
    print(hexStrSizHeight, " =>Hauteur Image =", int(big_endian_size_height, 16), " pixels")
   
    widthImage = int(big_endian_size_width, 16)
    heightImage = int(big_endian_size_height, 16)
    
    i=1
  #  while (i <= 1000):
    pixel_indice = 3*(pixel_num-1) + 54 + 1
    if (pixel_num == 0):
        print ("The parameter of the function colour_pixel (pixel_number) must not be 0 ! The minimum is 1")
    elif (pixel_num > widthImage*heightImage):
        print("The parameter of the function colour_pixel (pixel_number) must be less than ", int(big_endian_size_width, 16), " * ", int(big_endian_size_height, 16), " !")
    else:
        
        pixel_end = 54+ (int(big_endian_size_height,16)*int(big_endian_size_width,16)*3)+2
        for j in range(55, pixel_end+1):
            octet=f_lecture.read(1) #Lecture octet par octet
            if (big_endian_size_width != 0 and big_endian_size_height !=0 and j == pixel_indice):
                for num in range(0,3):
                    octets_size.append(octet)
                    hexStrPix = hexStrPix + " " + octet.hex()
                    octet=f_lecture.read(1) #Lecture octet par octet
   
    #stuff contains hexStrPix and widthImage and heightImage
    stuff = []
    stuff.append(hexStrPix)
    stuff.append(widthImage)
    stuff.append(heightImage)
    return stuff
      
#function that prints the color of the pixel
# nb_pixel: variable containing the number of pixel which we are looking for the RGB (There are 512*512 pixels for image "lena_couleur.bmp")
def affichage_Couleur_Pixel(nb_pixel, filename):
    hexDecPix=[] #variable containing the RGB of the pixel nb_pixel in decimal
    stuff = colour_pixel(nb_pixel, "lena_couleur.bmp")
   
    #We get hexStrPix
    hexStrPix = stuff[0]
    print("\nInfo of pixel number ", nb_pixel, ": ")
    print("RGB in hex=", hexStrPix)
    
    hexStrPix = hexStrPix.replace(" ", "") #on retire tous les espaces
    for m in range(0, len(hexStrPix), 2): #on prend les caracteres deux par deux
        code = hexStrPix[m:m+2]
        hexDecPix.append(int(code, 16)) #on convertit en decimal et on met dans la liste hexDec
    print("RGB in decimal=", hexDecPix)
    sizeImage = []
    #We get only the size of the image
    sizeImage.append(stuff[1])
    sizeImage.append(stuff[2])
   
    return sizeImage



sizeImage = affichage_Couleur_Pixel(int(args.colorPixel), filename)

#-------------affichage_Couleur_Pixel
if (args.colorPixel and int(args.colorPixel) != 0 and int(args.colorPixel) < sizeImage[0]*sizeImage[1]):  
    print("\n The color pixel you want to print is", args.colorPixel)
    sizeImage = affichage_Couleur_Pixel(int(args.colorPixel), filename)
    
elif(args.colorPixel and int(args.colorPixel) == 0):
    print("\n Error: The parameter colorPixel must not be 0 ! The minimum is 1 !")

elif(args.colorPixel and int(args.colorPixel) > sizeImage[0]*sizeImage[1]):
    print("\n Error: The parameter colorPixel must be less than ", sizeImage[0], " * ", sizeImage[1], " !")
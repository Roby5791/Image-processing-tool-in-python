# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 12:47:21 2021

@author: boris
"""

import argparse
import os
import sys

#Width of the image
widthImage = 0

#Height of the image
heightImage = 0

parser = argparse.ArgumentParser()
parser.add_argument("imageName", help="The relative path of the image. The root is where the program is.", type=str)

#----------------------------------------Arguments optionnels--------------------------------------

parser.add_argument("--colorPixel", help="Enter the color pixel of your image color. Ex: For a 515x512 color image, you can put 262144. NB: 0 <= colorPixel <= widthImage*heightImage")
parser.add_argument("--rotateDegree", help="Enter the degree of rotation of your image color. NB: This value must be 90, 180 or 270 ! Ex: 90")
parser.add_argument("--scaleFactor", help="Enter the scale factor of your image color. NB: This value must be between 1 and 10 ! Ex: 1")

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
    
    f_lecture.close
    
    global widthImage 
    global heightImage
    
    widthImage = int(big_endian_size_width, 16)
    heightImage = int(big_endian_size_height, 16)

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


#function which takes pixel number in input and output the hexa string of this pixel
def colour_pixel(pixel_num, filename):
    octets_size=[] #variable containing each octet of the picture (we will append after when we will look for the RGB in a for loop of a given number of pixel)

    hexStrPix="" #variable containing the RGB of the pixel nb_pixel in hex
    
    f_lecture =open(filename,'rb') #read in binary mode
    octet = bytes([0])
   
    i=1
    while (i <= 54):
        octet=f_lecture.read(1) #Lecture octet par octet
            
        i=i+1
    i=1

    pixel_indice = 3*(pixel_num-1) + 54 + 1
        
    pixel_end = 54+ (widthImage*heightImage*3)+2
 
    for j in range(55, pixel_end+1):
        octet=f_lecture.read(1) #Lecture octet par octet
        if (widthImage != 0 and heightImage !=0 and j == pixel_indice):
            for num in range(0,3):
                octets_size.append(octet)
                hexStrPix = hexStrPix + " " + octet.hex()
                octet=f_lecture.read(1) #Lecture octet par octet
    return hexStrPix

#function that prints the color of the pixel
# nb_pixel: variable containing the number of pixel which we are looking for the RGB (There are 512*512 pixels for image "lena_couleur.bmp")
def affichage_Couleur_Pixel(nb_pixel, filename):
    hexDecPix=[] #variable containing the RGB of the pixel nb_pixel in decimal
    hexStrPix = colour_pixel(nb_pixel, filename)
    print("\nInfo of pixel number ", nb_pixel, ": ")
    print("RGB in hex=", hexStrPix)
    
    hexStrPix = hexStrPix.replace(" ", "") #on retire tous les espaces
    for m in range(0, len(hexStrPix), 2): #on prend les caracteres deux par deux
        code = hexStrPix[m:m+2]
        hexDecPix.append(int(code, 16)) #on convertit en decimal et on met dans la liste hexDec
    print("RGB in decimal=", hexDecPix)
    
    

#function which rotates the image
def rotate_image(degres_rot, filename):
    
    f_lecture =open(filename,'rb') #read in binary mode
    outputName = "rotate_" + filename
    f_ecriture =open(outputName,'wb') #read in binary mode
    octet = bytes([0])
    
    entete_image=[]
   
    i=1
    while (i <= 54):
        octet=f_lecture.read(1) #Lecture octet par octet
        entete_image.append(octet)
            
        i=i+1
  
    i=1
      
    octets_s=[]
    octets_s_r=[]
    
    for i in range (widthImage):
        for j in range(heightImage):
            octets_s_r.append(f_lecture.read(3))
        octets_s.append(octets_s_r)
        octets_s_r = []
    
    for x in entete_image:
        f_ecriture.write(x)
    
    if(degres_rot==90):
        for i in range(widthImage):
            for j in range(heightImage):
                f_ecriture.write(octets_s[widthImage-1-j][i])
    elif(degres_rot==180):
        for i in range(widthImage):
            for j in range(heightImage):
                f_ecriture.write(octets_s[widthImage-i-1][heightImage-j-1])
    else:
        for i in range(widthImage):
            for j in range(heightImage):
                f_ecriture.write(octets_s[j][widthImage-i-1])
    
    f_lecture.close()
    f_ecriture.close()
    
    #print(octets_s_r)
    #print(len(octets_s_r))
 
#function which scales the image
def scale_image(scale, filename):
    
    f_lecture =open(filename,'rb') #read in binary mode
    outputName = "scale_" + filename
    f_ecriture =open(outputName,'wb') #read in binary mode
    octet = bytes([0])
    
    entete_image=[]
   
    i=1
    while (i <= 54):
        octet=f_lecture.read(1) #Lecture octet par octet
        entete_image.append(octet)
            
        i=i+1
    i=1
    
        
    octets_s=[]
    octets_s_r=[]
    scale_list=[]
    
    for i in range (widthImage):
        for j in range(heightImage):
            octets_s_r.append(f_lecture.read(3))
        octets_s.append(octets_s_r)
        octets_s_r = []
    
    for x in entete_image:
        f_ecriture.write(x)
   
    if(scale>0):
        for i in range(widthImage):
            for j in range(heightImage):
                for k in range(scale):
                    octets_s_r.append(octets_s[i][j])
                    #f_ecriture.write(octets_s[i][j])
            for l in range(scale):
                scale_list.append(octets_s_r)
            octets_s_r=[]
    else:
        print("The scale you enter must be positive !")
           
    for i in range(widthImage*scale):
        temp = scale_list[i]
        for j in temp:
            f_ecriture.write(j)
     
    f_lecture.close()
    f_ecriture.close()
    
    #print(octets_s_r)
    #print(len(octets_s_r))
    
#-------------ouverture_Fichiers_Image 
if (args.imageName[-3:] == "bmp"):
    sizeImage = ouverture_Fichiers_Image(filename)  
elif (args.imageName[-3:]=="png"):
    sizeImage = ouverture_Fichiers_Image_Png(filename)  

#-------------affichage_Couleur_Pixel
if (args.colorPixel and int(args.colorPixel) != 0 and int(args.colorPixel) <= widthImage*heightImage):  
    print("\n The color pixel you want to print is", args.colorPixel)
    affichage_Couleur_Pixel(int(args.colorPixel), filename)
    
elif(args.colorPixel and int(args.colorPixel) == 0):
    print("\n Error: The parameter colorPixel must not be 0 ! The minimum is 1 !")

elif(args.colorPixel and int(args.colorPixel) > widthImage*heightImage):
    print("\n Error: The parameter colorPixel must be less than ", sizeImage[0], " * ", sizeImage[1], " !")

#-----------rotation_Fichiers_Image
if (args.rotateDegree and (int(args.rotateDegree) == 90 or int(args.rotateDegree) == 180 or int(args.rotateDegree) == 270)):
    print("\n The degree of rotation you want to do is", args.rotateDegree) 
    rotate_image(int(args.rotateDegree), filename)
    outputName = "rotate_" + filename
    visualize(outputName)
elif (args.rotateDegree):
    print("\n Error: The parameter rotateDegree must be 90, 180 or 270 !")

#-----------scale_Fichiers_image
if (args.scaleFactor and int(args.scaleFactor) >= 1 and int(args.scaleFactor) <= 10):
    print("\n The factor of scale you want to do is", args.scaleFactor)
    scale_image(int(args.scaleFactor), filename)
    outputName = "scale_" + filename
    visualize(outputName)
elif(args.scaleFactor):
    print("\n Error: The parameter scaleFactor must be between 1 and 10 !")



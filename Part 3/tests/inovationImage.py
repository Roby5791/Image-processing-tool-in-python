# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 15:07:24 2021

@author: boris
"""

import argparse
import os
import sys
import numpy as np

#Width of the image
widthImage = 0

#Height of the image
heightImage = 0

parser = argparse.ArgumentParser()
parser.add_argument("imageName", help="The relative path of the image. The root is where the program is.", type=str)

parser.add_argument('--extractPartImage', nargs='+', help="There is 4 parameters ! \nEnter the position of the four edge and the height of the image you want to extract your image color. 1:left top X, 2: left top Y1, 3: right top Y2, 4: height wanted. \nNB: The first third positions must be between 0 and widthImage and the last inferior to (heightImage - first parameter). Ex: 50 75 500 50")
parser.add_argument('--filterImage', help="Enter the numero of the filter you want to apply to your image color.\n NB: 0: identity, 1: contour detection, 2: edge reinforcement, 3: pushback, 4: sharpen, 5: box blur, 6: gaussian blur \n 7: contrast add, 8: excessive edge detection, 9: emboss, 10: horizontal Sobel, 11 vertical Sobel")

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
    
    global widthImage 
    global heightImage
    
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
        #trioctets.append(octet)
        i = i+1
        octetsHex=""
        
    return trioctets
    f_lecture.close

#function which extract a part of the image
def extractPartImage(filename, leftTopX, leftTopY1, leftTopY2, heightWanted, trioctets):
    f_lecture =open(filename,'rb') #read in binary mode
    outputName = "extract_" + filename
    f_ecriture =open(outputName,'wb') #read in binary mode
    octet = bytes([0])
    
    widthPart = int(leftTopY2 - leftTopY1)
    heightPart = int(leftTopX + heightWanted)
    
    '''
    pad = 0; # Set pad byte count per row to zero by default.
    # Each row needs to be a multiple of 4 bytes.  
    if ((widthPart * 3) % 4 != 0):
        pad = 4 - ((widthPart * 3) % 4) # 4 - remainder(width * 3 / 4).
    
    '''
    
    i=1
    #Lecture du MAGIC NUMBER
    while (i <=54): #lecture Magic number sur 2 octets
        octet=f_lecture.read(1) #Lecture octet par octet
        if (i>=1 and i<=18): #size of the file in octets
            f_ecriture.write(octet)
        if (i==19): #print size of the picture's width
            f_ecriture.write(widthPart.to_bytes(4,'little'))
            #f_ecriture.write(int(widthPart+pad).to_bytes(4,'little'))
            i=i+3
            for k in range(3):
                octet=f_lecture.read(1) #Lecture octet par octet
        if (i==23): #print size of the picture's height
            f_ecriture.write(heightPart.to_bytes(4,'little'))
            for k in range(3):
                octet=f_lecture.read(1) #Lecture octet par octet
            i=i+3
        if (i>=27 and i<=54): #print number of planes in the image
            f_ecriture.write(octet)
        
        i = i+1
    
    trioctets = np.array(trioctets)
    tri = trioctets.reshape((widthImage,heightImage,3))   
   
    part=[]

    for m in range (leftTopX, heightPart):
        for n in range (leftTopY1, leftTopY2):
            part.append(tri[m][n])
            '''
            for padVal in range(pad):
                part.append(0)
            '''
    #count=0
    for i in part:
        #if i==0:
             #f_ecriture.write(int(0).to_bytes(1, 'little'))
        #count=count+1
        #if (count == heightPart):
             #for p in range(pad):
                 #f_ecriture.write(int(0).to_bytes(1,'little'))
        for j in i: 
               
            f_ecriture.write(int(j).to_bytes(1,'little'))
    '''       
    if ((widthPart * 3) % 4 != 0):
       pad = 4 - ((widthPart * 3) % 4) # 4 - remainder(width * 3 / 4).
    jj = pad * heightPart
    for m in range(jj):
        f_ecriture.write(int(0).to_bytes(1,'little'))
    '''
    siz=len(part)%4
    while (siz != 0):
        f_ecriture.write(int(0).to_bytes(1,'little'))
        siz=siz+1
        if (siz == 0):
            break
    
    
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

#function which apply a filter to the image
def filter_image(filterNum, filename):
    f_lecture =open(filename,'rb') #read in binary mode
    outputName = "filter_" + filename
    f_ecriture =open(outputName,'wb') #read in binary mode
    
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
    
    #identity
    if(filterNum == 0):
        kernel =  [[  0  , 0 ,   0],
                  [  0 ,   1 ,  0 ],
                  [  0  , 0 ,    0 ]]
    #contour detection
    elif(filterNum == 1):
        kernel =  [[  0  , 1 ,   0],
                  [  1 ,   -4 ,  1 ],
                  [  0  , 1 ,    0 ]]
    #edge reinforcement
    elif(filterNum == 2):
         kernel =  [[  0  , 0 ,   0],
                   [  -1 ,  1 ,   0],
                   [  0  , 0,    0 ]]
    #pushback       
    elif(filterNum == 3):
         kernel =  [[ -2  , -1 ,   0],
                   [  -1 ,  1 ,   1],
                   [  0  , 1,    2]]
    #sharpen          
    elif(filterNum == 4):
         kernel =  [[ 0  , -1 ,   0],
                   [  -1 ,  5 ,   -1],
                   [  0  , -1,    0]]
    #box blur
    elif(filterNum == 5):
        kernel =  [[ 1/9  , 1/9 ,   1/9],
                  [  1/9 ,  1/9 ,   1/9],
                  [  1/9  , 1/9,    1/9 ]]
    #gaussian blur 3*3           
    elif(filterNum == 6):
        kernel =  [[ 1/16  , 2/16 ,   1/16],
                   [ 2/16 ,  4/16 ,   2/16],
                   [  1/16  , 2/16,    1/16]]
        
    #contrast add          
    elif(filterNum == 7):
        kernel =  [[ 0  , -1 ,   0],
                   [ -1 ,  5 ,   -1],
                   [  0  , -1,    0]]   
    #excessive edge detection         
    elif(filterNum == 8):
        kernel =  [[ 1  , 1 ,   1],
                   [ 1 ,  -7 ,   1],
                   [ 1  , 1,    1]]
        
    #emboss          
    elif(filterNum == 9):
        kernel =  [[ -1  , -1 ,   0],
                   [ -1 ,  0 ,   1],
                   [  0  , 1,    1]]
        
    #horizontal Sobel        
    elif(filterNum == 10):
        kernel =  [[  1  , 0 ,   -1],
                  [  2 ,   0 ,  -2 ],
                  [  1  , 0 ,    -1 ]]
        
    #vertical Sobel         
    elif(filterNum == 11):
        kernel = [[ 1  , 2 ,   1],
                  [  0 ,   0 ,  0],
                  [  -1  , -2 ,  -1 ]]
        
    
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
    trioctets = ouverture_Fichiers_Image(filename)  
    
#-------------extractPartImage
if (args.extractPartImage and len(args.extractPartImage) == 4 and int(args.extractPartImage[0]) >= 0 and int(args.extractPartImage[0]) <= widthImage and int(args.extractPartImage[1]) >= 0 and int(args.extractPartImage[1]) <= widthImage and int(args.extractPartImage[2]) >= 0 and int(args.extractPartImage[2]) <= heightImage and int(args.extractPartImage[3]) >= 0 and int(args.extractPartImage[3]) <= heightImage and int(args.extractPartImage[2]) > int(args.extractPartImage[1]) and int(args.extractPartImage[3]) <= (int(widthImage) - int(args.extractPartImage[0])) ):    
    print("\n The values of the edge you want to extract from the color image are: ", int(args.extractPartImage[0]), int(args.extractPartImage[1]), int(args.extractPartImage[2]), int(args.extractPartImage[3]))
    extractPartImage(filename, int(args.extractPartImage[0]), int(args.extractPartImage[1]), int(args.extractPartImage[2]), int(args.extractPartImage[3]), trioctets) 
    outputName = "extract_" + filename
    #visualize(outputName)
elif (args.extractPartImage and len(args.extractPartImage) == 4 and not(int(args.extractPartImage[0]) >= 0 and int(args.extractPartImage[0]) <= widthImage and int(args.extractPartImage[1]) >= 0 and int(args.extractPartImage[1]) <= widthImage and int(args.extractPartImage[2]) >= 0 and int(args.extractPartImage[2]) <= heightImage and int(args.extractPartImage[3]) >= 0 and int(args.extractPartImage[3]) <= heightImage and int(args.extractPartImage[2]) > int(args.extractPartImage[1]) and int(args.extractPartImage[3]) <= (int(widthImage) - int(args.extractPartImage[0])) )):   
#elif (args.extractPartImage and len(args.extractPartImage) == 4 and (int(args.extractPartImage[0]) < 0 or int(args.extractPartImage[0]) > widthImage or int(args.extractPartImage[1]) < 0 and int(args.extractPartImage[1]) > widthImage and int(args.extractPartImage[2]) < 0 or int(args.extractPartImage[2]) > heightImage or int(args.extractPartImage[3]) < 0 or int(args.extractPartImage[3]) > heightImage or int(args.extractPartImage[0]) >= int(args.extractPartImage[1]) or int(args.extractPartImage[4]) >= int(args.extractPartImage[2]))):  
    print("\n Error: The first and second parameters of the edge must be between 0 and ", widthImage, " !")  
    print("\n Error: The third and fourth parameters of the edge must be between 0 and ", heightImage, " !")  

elif(args.extractPartImage and (len(args.extractPartImage) == 1 or len(args.extractPartImage) == 2 or len(args.extractPartImage) == 3)):
    print("\n Error: You must enter four parameters !")
    
#-----------filterImage
if (args.filterImage and int(args.filterImage) >= 0 and int(args.filterImage) <= 11):
    print("\n The number of the filter you want to apply to the color image is: ", args.filterImage)
    filter_image(int(args.filterImage), filename)
    outputName = "filter_" + filename
    visualize(outputName)
#The value of filter will be between 0 and 11
elif (args.filterImage and int(args.filterImage) < 0 and int(args.contrastImage) > 11):
    print("The value of the number of the bilter must be between 0 and 11")
elif(args.filterImage):
    print("\n Error: The parameter filterImage must be between 0 and 11 !")
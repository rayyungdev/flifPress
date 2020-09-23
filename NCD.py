from ctypes import *
import os
from matplotlib import pyplot as py
import numpy as np
from PIL import Image

def imList(im): 
    if not isinstance(im, list):
        X=[] #Create an empty list to store the numpy array (image)
        if(len(np.shape(im)) > 2): #This is explicitly used for the gnist class. 
            #Current gnist functions return an image with 
            for ima in im:
                X.append(ima)
        else:
            X.append(im) #Store the image in a list (For future preparation when we need to import multiple images)
    else: 
        X=im.copy()
    return X
    
def flifPress(im):
    
    LIB = CDLL ("./lib/libflif.dll") #import libflif library
    X=imList(im) #Function shown above, appends images to a list. Currently WORKS. 
    
    ####     Zero Padding:
    [FW2, FH2] = max(np.shape(matx) for matx in X); #Find the largest dimensions in the list of images. 
    
    for i in range(len(X)):
        [curW, curH] = np.shape(X[i]); #Current W/H
        padW = FW2 - curW +1; padH = FH2 - curH+1; #Difference between the max and the current dimensions + 1
        X[i] = np.pad(X[i],((0,padW),(0,padH)))
        
    X = np.asarray(X) #Convert back the list to a numpy array because calculations run faster 
    
    ######## Start up FLIF #################
    create_enc = LIB.flif_create_encoder #Set up function 
    create_enc.restype = POINTER(c_void_p) #Create new pointer class to return void pointer. 
    enc = create_enc() #Actually start up FLIF
    
    import_image_GRAY=LIB.flif_import_image_GRAY #Set up import gray image function from FLIF library.
    import_image_GRAY.restype=POINTER(c_void_p) #Designate to return a memory encoded pointer. 
    fim=[] #Flif Pointer. However, may need to fix this later as it currently returns void pointers as FLIF_pointers is a custom pointer
    
    for count in range(len(X)):
        [W, H] = np.shape(X[count]) #New Width/New Height of Image (could be shortened to just FW2+1 & FH2+1)
        pim = X[count].ctypes.data_as(c_void_p); #PIM is the pointer to the current image.
        
        temp=import_image_GRAY(W, H, pim, W) #Current flif pointer
        fim.append(temp) #Append the flif pointer into the FIM list. 
        
        encoder_add_image_move= LIB.flif_encoder_add_image_move
        encoder_add_image_move(enc, fim[count]) #Use function to return a pointer
            
    #####For Output##########
    pdest=pointer(c_uint8())#Setting up Double Pointer. Will need to pass this on as a byref for double pointer
    prsz=c_void_p(0);
    
    encode_mem=LIB.flif_encoder_encode_memory
    encode_mem(enc, byref(pdest), byref(prsz))
    nBytes=prsz.value
    
    #########Clean Up#######################
    for fimi in fim: 
        LIB.flif_destroy_image(fimi)
    LIB.flif_destroy_encoder(enc)
    LIB.flif_free_memory(pdest)
    return nBytes

def imNCDM(X):
    if not isinstance(X, list):
        raise TypeError('input X requires a list of images')
    if len(X) <= 1:
        return 0 
    
    GX = flifPress(X); #Total bytes for entire image list. 
    cxi = [flifPress(x) for x in X] #Fliff press individual images in the list
    
    cxi = np.asarray(cxi)
    gx= np.min(cxi)
    
    gExclude = []
    
    for ni in range(len(X)):
        xExclude = X.copy()
        del xExclude[ni] #Remove the particular image at this index
        gExclude.append(flifPress(xExclude))
        
    return ((GX - gx) / np.max(np.asarray(gExclude)))
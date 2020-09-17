#!/usr/bin/env python
# coding: utf-8

# In[1]:
import numpy as np
from matplotlib import pyplot as plt
import idx2numpy
import random as rand
from NCD import *
from PIL import Image
import cv2 as cv2
import pandas as pd
import multiprocessing as mp


# # gnist is a class that opens ubyte image files and reads them. 
# 
# To initialize gnist, you need to input the image and label paths, otherwise it defaults.  
# Might be able to convert the entire app folder and attach it to this class

# In[2]:


class gnist:
    def __init__(self, image_path = None, label_path = None):
        ###    Set Image/Label Path otherwise it defaults to the handwritten digits file
        if (not image_path and not label_path):
            image_path = './lib/train-images.idx3-ubyte'
            label_path = './lib/train-labels.idx1-ubyte'
        #Import images directly with the idx2numpy library
        (self.images, self.labels) = (idx2numpy.convert_from_file(image_path), idx2numpy.convert_from_file(label_path))
    
    def show(self, index):
        #Function allows you to call a particular image from the dataset using it's index. 
        if not isinstance(index, int):
            raise TypeError('index requires int')
            
        #Binarize the image
        thresh, grayImage = cv2.threshold(self.images[index], 0, 255, cv2.THRESH_BINARY) #work around gray2ind
        
        image = grayImage; label = self.labels[index];
        plt.figure;
        plt.imshow(image, cmap = 'gray')
        plt.title('Label: ' + str(label), fontsize = 20, fontweight = 'bold');
        return image
    
    def training(self, nsamples):
        if not isinstance(nsamples, int):
            raise TypeError('nsamples requires int')
            
        Training = [];
        Stored = [];
        while len(Training) < nsamples *10:
            i = round(len(self.images)*rand.random())
            
            if (self.images[i].all, self.labels[i].all) in Training:
                #Check if the data set was already inputed into the dataset
                continue
                
            if Stored.count(self.labels[i]) >= nsamples:
                #Maintain Uniform distribution of true labels
                continue
                
            nt = {}
            #### Preprocess image
            thresh, grayImage = cv2.threshold(self.images[i], 0, 255, cv2.THRESH_BINARY) #work around gray2ind
            nt['label'] = self.labels[i]
            nt['im'] = grayImage
            nt['i'] = i
            Stored.append(self.labels[i])
            Training.append(nt)
        return np.asarray(Training)
    
    def getmnist(self, target, cardinality):
        if not isinstance(target, np.ndarray):
            raise TypeError('target requires numpy array')
            
        #Import Training Set using gnist().training
        M = self.training(cardinality)
        
        Training = sorted(M, key = lambda i: i['label'])
        reTrain = []; idxGT = [];
        
        for index in Training:
            if index['label'] in target:
                reTrain.append(index)
                idxGT.append(index['label']+1)
        return np.asarray(reTrain), np.asarray(idxGT)
    
    def mnistdistance(self, Training):
        d = np.zeros((len(Training), len(Training)))
        for i in range(len(Training)):
            for j in range(len(Training)):
                if (i == j):
                    continue
                d[i,j] = imNCDM([Training[i]['im'], Training[j]['im']])
            
        return Regularize(d)[0]


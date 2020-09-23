import numpy as np
from matplotlib import pyplot as plt
import idx2numpy
import random as rand
from NCD import *
from PIL import Image
import cv2 as cv2
import pandas as pd
from Cluster import *

class gnist:
    def __init__(self, image_path = None, label_path = None):
        ###    Set Image/Label Path otherwise it defaults to the handwritten digits file
        if (not image_path and not label_path):
            image_path = './lib/train-images.idx3-ubyte'
            label_path = './lib/train-labels.idx1-ubyte'
        #Import images directly with the idx2numpy library
        #Using the initialized function to call the image is not recommended as it's the raw image file, prior to preproccessing the image for fliffpress
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
                #Check if the data set was  already inputed into the dataset
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
    
    def getmnist(self, targ, cardinality):
        if not (isinstance(targ, np.ndarray) or isinstance(targ, list)):
            raise TypeError("Input Targ requires list or numpy array")
        target = np.asarray(targ) if isinstance(targ, list) else targ
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

if __name__ == "__main__":
    target = [0,1]
    cardinality = 10
    TrainSet, idxGT = gnist().getmnist(target, cardinality)
    print(TrainSet)
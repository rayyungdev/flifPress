# flifPress
https://github.com/FLIF-hub/FLIF - Free losless image libary 
## Set Up
Set up your virtual environment by using virtualenv
In your virtual env, install the requirements with
##### pip install -r requirements.txt
Once the necessary libaries are set up, you should be able to run functions from gnist.py and NCD.py.
Note, if you're running from the command line, you will not be able to see the images (I suggest running from jupyter). However, the calculations will still work

## Functions
This repository contains two different files:  
gnist.py -- Main file, which utilizes NCD.py - used to pull training data. Contains one class, gnist.   
NCD.py -- contains functions pertaining FLIF library as well as other auxillary functions (imList, flifPress, imNCDM, Regularize). This file utilizes the FLIF library. 
### Usage of gnist.py/ipynb (See jupyter notebook for example usage)
gnist(image_path, label_path) - class function that pulls image/label data from a ubyte file in your working directory. If no path for the image/label is entered as paramater, it defaults to the hand written digits files found in the working directory's library.
  
gnist().show(index) - If you know the particular image's index you want to pull from the file, you may use this function to pull the data pertaining to that image. This function will also show you that particular image.  
  
gnist().training(nsamples) - Creates a randomized but uniformly distributed training set.   
  
gnist().getmnist(target, cardinality) - Creates a training set based off target and cardinality
  
gnist().getmnistdistance(Training) - Returns distance matrix for the particular training set.  

### Running from command line
Open up your python terminal and import gnist
##### from gnist import *
Once this is done, you will be able to run any of the gnist or NCD file from the command line. Please note, you will not be able to view images unless you have already set up a default viewer for your console

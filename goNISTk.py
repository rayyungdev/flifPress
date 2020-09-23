from NCD import *
from Cluster import *
from apps import getmnist
import numpy as np

target = [0,1]
cardinality = 10

for n in range(100):
    xDigits = getmnist().getmnist(target, cardinality)
    dDigits = getmnist().mnistdistance(xDigits[0])

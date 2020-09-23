import numpy as np


def Regularize(DistanceMat):
    D = DistanceMat;
    W, H = np.shape(D)
    for i in range(W):
        for j in range(H):
            D[i,j] = np.max((D[i,j], D[j,i]));
        D[i,i] = 0;
    bound = D;
    bW, bH = np.shape(bound);
    for i in range(bW):
        bound[i,i] = 0;
    a = np.min(bound)
    degenerate = 1 if a == 0 else 0
    return D, degenerate;
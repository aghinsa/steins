import numpy as np
import os
import glob
import cv2

def get(parent):
    parent="/home/aghinsa/Documents/insti/fellow/datasets/lfw"
    keep=5
    count=0
    x=[]
    y=[]
    sub=glob.glob(parent+'/*')
    # print(sub)
    for folder in sub:
        temp=glob.glob(folder+'/*')
        if len(temp)>=2:
            count+=1
            if(count)>=keep:
                break
            for file in temp:
                x.append(cv2.imread(file))
                y.append(count)
    x=np.reshape(np.asarray(x),(len(y),-1))
    x=x[:,:128]
    y=np.reshape(np.asarray(y),(-1,1))
    return x,y

import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt



def getObjectPoints(dim):
    """
    Input:tuple of x,y (x,y)
    return:ndarray
    get 3d coordinates for checkboards

    """
    points=np.zeros((dim[0]*dim[1],3),np.float32)
    points[:,:2]=np.mgrid[0:dim[0],0:dim[1]].T.reshape(-1,2)
    return points

def getImagePoints(img,dim,visualise=False):
    """
    input:image(ndarray),dim=(x,y),visualise(bool,default=false)
    returns:imagePoints(ndarray)
    """
    if(img.ndim==3):
        img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    else:
        img_gray=img
    condition=(cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER,30,0.01)
    ret,corners=cv2.findChessboardCorners(img_gray,dim,None)
    if(ret==True):
        corners_refined=cv2.cornerSubPix(img_gray,corners,(11,11),(-1,-1),condition)
        if visualise==True:
            cv2.imshow('pattern',cv2.drawChessboardCorners(img,dim,corners_refined,ret))
            cv2.waitKey()
        return corners_refined.astype(np.float32)
    return np.zeros(3)

def calibrateCamera(chessDir,dim):
    """
    input:path of directory of images,pattern dimension (tuple)
    return:ret,cameraMatrix,distortion,rotationVec,translationVec
    """
    images=glob.glob(os.path.join(chessDir,'*'))
    points=getObjectPoints(dim)
    realPoints=[]
    imagePoints=[]

    for file in images:
        img=cv2.imread(file)
        cornerPoints=getImagePoints(img,dim)
        imgsize=(img.shape[0],img.shape[1])
        if(cornerPoints.shape!=(3,)):
            realPoints.append(points)
            imagePoints.append(cornerPoints.astype(np.float32))
    ret,cameraMatrix,distortion,rotationVec,translationVec=cv2.calibrateCamera(realPoints,imagePoints,imgsize,None,None)
    return (ret,cameraMatrix,distortion,rotationVec,translationVec)
    #return cameraMatrix

def checkDimensions(img,top):
    """
    input:images
    return:null
    print dims detected till top
    """
    for i in range(3,top+1):
        for j in range(3,top+1):
            ret,corners=cv2.findChessboardCorners(img,(i,j),None)
            if ret==True:
                print('({},{})'.format(i,j))
    return

def convertColor(img,target='RGB'):
    if target=='RGB':
        return cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    elif target=='GRAY':
        return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

def computeFeatures(img):
    sift=cv2.xfeatures2d.SIFT_create()
    if img.ndim==3:
        kp,desc=sift.detectAndCompute(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY),None) #none is th mask
    else:
        kp,desc=sift.detectAndCompute(img,None)
    return (kp,desc)

def computeMatches(desc1,desc2,crossCheck=False):
    matcher=cv2.BFMatcher( cv2.NORM_L2,crossCheck)
    matches=matcher.knnMatch(desc1,desc2,k=2)
    return matches

def ratioTest(matches,kp1,kp2,ratio=0.75):
    """
    returns,goodMatches,pts1,pts2 (alignes points)
    """
    good=[]
    pts1=[]
    pts2=[]
    for i,(m,n) in enumerate(matches):
        if m.distance<0.75*n.distance:
            good.append(m)
            pts2.append(kp2[m.trainIdx].pt)
            pts1.append(kp1[m.queryIdx].pt)
    return good,pts1,pts2

def computeEssentialMat(pts1,pts2,cameraMat):
    pts1_norm=cv2.undistortPoints(np.expand_dims(pts1,axis=1),cameraMatrix=cameraMat,distCoeffs=None)
    pts2_norm=cv2.undistortPoints(np.expand_dims(pts2,axis=1),cameraMatrix=cameraMat,distCoeffs=None)
    E, mask = cv2.findEssentialMat(pts1_norm,pts2_norm, focal=1.0, pp=(0., 0.), method=cv2.RANSAC, prob=0.999, threshold=3.0)
    return E

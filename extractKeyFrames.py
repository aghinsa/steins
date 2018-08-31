import os
import cv2
import sys
import argparse
from skimage.measure import compare_ssim as ssim 

def get_arg(args):
    parser=argparse.ArgumentParser(description='extracting key frames')
    parser.add_argument('-i','--input',type=str,required='True',help='input dir')
    #parser.add_argument('-o','--output',type=str,default='~',help='output dir')
    #results=parser.parse_args(args)
    #vars is a function which return the __dict__ if the argument
    #return vars(parser.parse_args(args))
    return parse.parse_args(args).input

def extractKeyFrames(videoIn):
    inDir=videoIn.split('/')
    outDir=os.path.join(os.path.expanduser('~'),'/'.join(inDir[1:-1]),inDir[-1].split('.')[0])
    try:
        os.makedirs(outDir) #makes a dir with videoname
    except:
        pass
    cap=cv2.VideoCapture(os.path.join(os.path.expanduser('~'),'/'.join(inDir[1:-1]),inDir[-1]))
    ret,prev_frame=cap.read()
    c=1
    print('extracting....')
    while ret:
        ret,curr_frame=cap.read()
        score=ssim(prev_frame,curr_frame,multichannel=True)
        print(score)
        if (score<0.8):
            cv2.imwrite(os.path.join(outDir,'{}.jpg'.format(c)),curr_frame)
            c+=1;
        prev_frame=curr_frame
    print('extracted {} frames and saved to {} '.format(c,outDir))

if __name__="main":
    videoIn=get_arg(argv[1:])
    extractKeyFrames(videoIn)
    



        


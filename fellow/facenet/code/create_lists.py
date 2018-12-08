import os
import numpy as np
import argparse
import glob

"""
creates:
    class_list.txt
    pair_list.txt
    non_pair_list.txt
    
    content in all the text files is of the format
        
        path_to_image label
        
example:
    python create_lists -i path_to_dataset -c trig
trig: 1:to create class_list.txt (default)
      0:else 
        if trig==0 class_list.txt should exist


"""

def get_pairs(parent_dir):
    sub=glob.glob(parent_dir+'/*')
    l=[]
    count=0
    for folder in sub:
        temp=glob.glob(folder+'/*')
        if len(temp)>=2:
            l.append(folder)
            count+=len(temp)
    print("Pair details:")
    print("\tNumber of people : {}".format(len(l)))
    print("\tNumber of images : {}".format(count))
    return l
def create_class_list (parent_dir):
    f=open("class_list.txt","w+")
    sub=glob.glob(parent_dir+'/*')
    class_name=0
    for folder in sub:
        class_name+=1
        temp=glob.glob(folder+'/*')
        for image in temp:
            f.write("{} {}".format(image,class_name))
            f.write('\n')
    f.close()

def create_pair_list(parent_dir,labels):
    l=get_pairs(parent_dir)
    f=open('pair_list.txt','w+')
    for folder in l:
        files=glob.glob(folder+'/*')
        for image in files:
            tag=image.split('/')[-1]
            label=labels[tag]
            f.write('{} {}'.format(image,label))
            f.write('\n')
    f.close()
def create_non_pair_list(parent_dir,labels):
    sub=glob.glob(parent_dir+'/*')
    l=[]
    count=0
    for folder in sub:
        temp=glob.glob(folder+'/*')
        if len(temp)==1:
            l.append(folder)
            count+=len(temp)
    print("Non-Pair details:")
    print("\tNumber of people : {}".format(len(l)))
    print("\tNumber of images : {}".format(count))
    
    f=open('non_pair_list.txt','w+')
    for folder in l:
        files=glob.glob(folder+'/*')
        for image in files:
            tag=image.split('/')[-1]
            label=labels[tag]
            f.write('{} {}'.format(image,label))
            f.write('\n')
    f.close()


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--input_dir","-i")
    parser.add_argument("--create","-c",type=int,default=1)
    args=parser.parse_args()
    parent_dir=args.input_dir
    if(args.create):
        create_class_list(parent_dir)
    #creating labels dict
    labels={}
    f=open("class_list.txt","r")
    for line in f:
        line=line.split()
        labels[line[0].split('/')[-1]]=line[1]
    f.close()
    ####
    create_pair_list(parent_dir,labels)
    create_non_pair_list(parent_dir,labels)
    
    
    
    
    

    

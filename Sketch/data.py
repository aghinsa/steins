import os
import tensorflow as tf
import numpy as np
import cv2
import config

main_dir=config.main_dir
training_iter=config.training_iter
batch_size=config.batch_size
learning_rate=config.learning_rate

def file_to_list(text):
    f=open(text,'r')
    text_list=[]
    for line in f:
        text_list.append(line[0:-1])
    f.close()
    return text_list

def normalize_image(image):
	# normalize to [-1.0, 1.0]
	if image.dtype == np.uint8:
		return image.astype("float")/127.5-1.0
	elif image.dtype == np.uint16:
		return image.astype("float")/32767.5-1.0
	else:
		return image.astype("float")
def read_sketch(source_directory,value,size=256):
    #value 0 to 3
    """
    direcorty:main/sketch/
    view:f s
    return: size x size x 2
    """
    # temp=np.empty((size,size))
    f_dir=os.path.join(source_directory,'sketch-F-{}.png'.format(value))
    c0=cv2.imread(f_dir,0)
    print(c0.dtype)
    c0=normalize_image(c0)
    s_dir=os.path.join(source_directory,'sketch-S-{}.png'.format(value))
    c1=cv2.imread(s_dir,0)
    c1=normalize_image(c1)
    temp=np.dstack((c0,c1))
    return temp

def read_dnfs(target_directory,view,size=256):
    """
    direcorty:main/dnfs/subject
    view:0 .. 11
    return size x size x 5
    """
    # temp=np.empty((size,size))
    encoded=cv2.imread(os.path.join(target_directory,"dn-256-{}.png".format(view)),cv2.IMREAD_UNCHANGED)
    mask=encoded[:,:,0]>0.9
    temp=np.dstack((normalize_image(encoded[:,:,0]),normalize_image(encoded[:,:,1]),normalize_image(encoded[:,:,2])))
    temp=np.dstack((temp,normalize_image(encoded[:,:,3])))
    temp=np.dstack((temp,mask))
    return temp

def get_subject_source(name,value=0):
    #main dir is global
    sketch=os.path.join(main_dir,'sketch',name)
    source=read_sketch(sketch,value)
    return source
def get_subject_target(name,view=0):
    dnfs=os.path.join(main_dir,'dnfs',name)
    target=read_dnfs(dnfs,view)
    return target

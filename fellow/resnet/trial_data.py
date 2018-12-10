import tensorflow as tf 
import cv2
import numpy as np
from imgaug import augmenters as iaa
import argparse

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

def _setter(filename,label):
    """
    images :image path
    """
    # image_string=tf.read_file(filename)
    # image=tf.image.decode_jpeg(image_string)
    image=cv2.imread(filename)
    image=cv2.cvtColor(gray,cv2.COLOR_BGR2RGB)
    seq = iaa.Sequential([
        iaa.Crop(px=(0, 16)),iaa.Fliplr(0.5),iaa.GaussianBlur(sigma=(0, 3.0))])
    image_aug = seq.augment_images(image)
    return image,label

# def _augment(image,label):
#     seq = iaa.Sequential([
#         iaa.Crop(px=(0, 16)),iaa.Fliplr(0.5),iaa.GaussianBlur(sigma=(0, 3.0))])
#     images_aug = seq.augment_images(images)
    
def custom_input_fn(data_dir, batch_size,):
    
    create_class_list(data_dir)
    
    f=open('class_list.txt','r')
    filenames=[]
    labels=[]
    for line in f:
        line=line.split()
        filenames.append(line[0])
        labels.append([line[1]])
    f.close()
    
    dataset=tf.data.Dataset.from_tensor_slices((filenames,labels))
    
    dataset=dataset.apply(tf.contrib.data.map_and_batch(
                lambda filename,label:tf.py_func(_setter,[filename,label],[tf.uint8,label.dtype]),
                batch_size,
                num_parallel_batches=4,)
                )
    # datasset=dataset.map(_setter)
    # dataset=dataset.batch(batch_size)
    dataset = dataset.prefetch(buffer_size=batch_size)
    return dataset

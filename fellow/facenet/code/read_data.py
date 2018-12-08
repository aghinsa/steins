import tensorflow as tf 
import cv2
import numpy as np



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
    image_string=tf.read_file(filename)
    image=tf.image.decode_jpeg(image_string)
    return image,label
    
def input_fn(is_training, data_dir, batch_size, num_epochs=1, num_gpus=None,
             dtype=tf.float32):
    
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
    
    dataset=dataset.apply(tf.contrib.data.map_and_batch(_setter,batch_size,
                        num_parallel_batches=4,))
    # datasset=dataset.map(_setter)
    # dataset=dataset.batch(batch_size)
    dataset = dataset.prefetch(buffer_size=batch_size)
    return dataset

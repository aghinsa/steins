"""
python3 resnet.py -i path_to_dataset
"""

import resnet_model
import tensorflow as tf
import numpy as np 
import argparse
import data
import triplet_loss

BATCH_SIZE=4
RESNET_SIZE=18
NUM_CLASSES=400
RESNET_VERSION=1
DTYPE=tf.float32
TRAINING=True

def _get_block_sizes(resnet_size):
  """Retrieve the size of each block_layer in the ResNet model.

  The number of block layers used for the Resnet model varies according
  to the size of the model. This helper grabs the layer set we want, throwing
  an error if a non-standard size has been selected.

  Args:
    resnet_size: The number of convolutional layers needed in the model.

  Returns:
    A list of block sizes to use in building the model.

  Raises:
    KeyError: if invalid resnet_size is received.
  """
  choices = {
      18: [2, 2, 2, 2],
      34: [3, 4, 6, 3],
      50: [3, 4, 6, 3],
      101: [3, 4, 23, 3],
      152: [3, 8, 36, 3],
      200: [3, 24, 36, 3]
  }

  try:
    return choices[resnet_size]
  except KeyError:
    err = ('Could not find layers for selected Resnet size.\n'
           'Size received: {}; sizes allowed: {}.'.format(
               resnet_size, choices.keys()))
    raise ValueError(err)

def embed_normal(images,labels,model,shape=(-1,250,250,3)):
  """
  cast images to float 32 and normalises
  return:normalized embeding (?,250,250,3)
  """

  images=tf.reshape(images,shape)
  labels=tf.reshape(labels,(-1,1))
  images=tf.cast(images,dtype=tf.float32)
  labels=tf.strings.to_number(labels)
  embedings=model.__call__(images,training=TRAINING)
  embedings=tf.nn.l2_normalize(images,axis=0)
  return embedings,labels

                
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--input_dir","-i")
    args=parser.parse_args()
    data_dir=args.input_dir

    sess=tf.Session()
    model=resnet_model.Model(resnet_size=RESNET_SIZE,bottleneck=False, 
                num_classes=NUM_CLASSES, 
                num_filters=64,kernel_size=7,conv_stride=2, 
                first_pool_size=3, first_pool_stride=2,
                block_sizes=_get_block_sizes(RESNET_SIZE), 
                block_strides=[1, 2, 2, 2],
                resnet_version=RESNET_VERSION, data_format=None,
                dtype=DTYPE,
                sess=sess)
    
    print("starting")
    dataset=data.custom_input_fn(data_dir,batch_size=BATCH_SIZE)
    iterator=dataset.make_initializable_iterator()
  
    it_init=iterator.initializer
    tf_init_g=tf.global_variables_initializer()
    tf_init_l = tf.local_variables_initializer()
    sess.run(it_init)
    images,labels=iterator.get_next()
    embedings,labels=embed_normal(images,labels,model=model)
    
    
    sess.run(tf_init_g)
    sess.run(tf_init_l)
    
    print(embedings)
    print(labels)
    loss=triplet_loss.hard_triplet_loss(embedings,labels,margin=0.3,k=1)
    print(loss)
    
    

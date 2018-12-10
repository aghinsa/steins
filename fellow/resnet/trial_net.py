import resnet_model
import tensorflow as tf
import numpy as np 
import argparse
import trial_data

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
    

model=resnet_model.Model(resnet_size=RESNET_SIZE,bottleneck=False, num_classes=NUM_CLASSES, 
                num_filters=64,kernel_size=7,conv_stride=2, 
                first_pool_size=3, first_pool_stride=2,
                block_sizes=_get_block_sizes(RESNET_SIZE), 
                block_strides=[1, 2, 2, 2],
                resnet_version=RESNET_VERSION, data_format=None,
                dtype=DTYPE)
                
                
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--input_dir","-i")
    args=parser.parse_args()
    data_dir=args.input_dir
    
    print("starting")
    dataset=trial_data.custom_input_fn(data_dir,batch_size=BATCH_SIZE)
    iterator=dataset.make_initializable_iterator()
    print("geting data")
    initi=iterator.initializer
    images,labels=iterator.get_next()
    print("got data")
    # images=images.set_shape(tf.TensorShape([BATCH_SIZE,250,250,3]))
    print(images.shape)
    #
    
    sess=tf.Session()
    sess.run(initi)
  
    img=sess.run(images)
    img=img.astype(np.uint8)
    img=tf.convert_to_tensor (img)
    print(img.shape)
    _outs=model.__call__(img,training=TRAINING)
    out=sess.run(_outs)
    

import numpy as np
import tensorflow as tf
import tensorflow.contrib.layers as tf_layers
import config

main_dir=config.main_dir
training_iter=config.training_iter
batch_size=config.batch_size
learning_rate=config.learning_rate

def encoderNdecoder(images,out_channels=5,normalizer_fn=tf_layers.batch_norm,activation=tf.nn.leaky_relu):
    """
    images:n*h*x*c
    """

    e1=tf_layers.conv2d(images,num_outputs=64,kernel_size=4,stride=2,normalizer_fn=normalizer_fn,activation_fn=tf.nn.leaky_relu) #128x128x64
    e2=tf_layers.conv2d(e1,num_outputs=128,kernel_size=4,stride=2,normalizer_fn=normalizer_fn,activation_fn=tf.nn.leaky_relu) #64x64x128
    e3=tf_layers.conv2d(e2,num_outputs=256,kernel_size=4,stride=2,normalizer_fn=normalizer_fn,activation_fn=tf.nn.leaky_relu) #32x32x256
    e4=tf_layers.conv2d(e3,num_outputs=512,kernel_size=4,stride=2,normalizer_fn=normalizer_fn,activation_fn=tf.nn.leaky_relu) #16x16x512
    e5=tf_layers.conv2d(e4,num_outputs=512,kernel_size=4,stride=2,normalizer_fn=normalizer_fn,activation_fn=tf.nn.leaky_relu) #8x8x512
    e6=tf_layers.conv2d(e5,num_outputs=512,kernel_size=4,stride=2,normalizer_fn=normalizer_fn,activation_fn=tf.nn.leaky_relu) #4X4X512
    encoded=tf_layers.conv2d(e6,num_outputs=512,kernel_size=4,stride=2,normalizer_fn=normalizer_fn,activation_fn=tf.nn.leaky_relu) #2X2X512
    print(encoded.get_shape().as_list())
    d6=tf_layers.dropout(upsample(encoded,512)) #4X4x512
    print(d6.get_shape())
    d5=tf_layers.dropout(upsample(tf.concat([d6,e6],3),512)) #8X8X512
    d4=upsample(tf.concat([d5,e5],3),512) #16x16x512
    d3=upsample(tf.concat([d4,e4],3),256) #32x32x256
    d2=upsample(tf.concat([d3,e3],3),128) #64x64x128
    d1=upsample(tf.concat([d2,e2],3),64) #128x128x64

    decoded=upsample(tf.concat([d1,e1],3),out_channels) #256x256x5

    return decoded



def upsample(x,n_channels,kernel=4,stride=2,activation_fn=tf.nn.leaky_relu,normalizer_fn=tf_layers.batch_norm):
    """
    x is encoded
    """
    h_new=(x.get_shape()[1].value)*stride
    w_new=(x.get_shape()[2].value)*stride
    up=tf.image.resize_nearest_neighbor(x,[h_new,w_new])

    return tf_layers.conv2d(up,num_outputs=n_channels,kernel_size=kernel,stride=1,normalizer_fn=normalizer_fn,activation_fn=activation_fn)


# def Unet(images,out_channels=5,batch_size=2):
#     decoded=encoderNdecoder(images,out_channels)
#     return decoded

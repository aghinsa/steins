import tensorflow as tf
import numpy as np
import os

import config
config.init()

import model
import loss
import data

main_dir=config.main_dir
training_iter=config.training_iter
batch_size=config.batch_size
learning_rate=config.learning_rate
name_list_path=config.name_list_path

name_list=data.file_to_list(name_list_path)

images=tf.placeholder("float",shape=[None,256,256,2])
truth=tf.placeholder("float",shape=[None,256,256,5])

pred=model.encoderNdecoder(images)
cost=loss.total_loss(pred,truth)
optimizer=tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
init=tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    for i in range(training_iter):
        for batch in range(len(name_list)//batch_size):
            batch_list=name_list[batch*batch_size:min((batch+1)*batch_size,len(name_list))]
            batch_x=list(map(data.get_subject_source,batch_list))
            batch_y=list(map(data.get_subject_target,batch_list))
            opt=sess.run(optimizer,feed_dict={images:batch_x,truth:batch_y})
            loss=sess.run(cost,feed_dict={images:batch_x,truth:batch_y})
        print("iter "+str(i)+" loss ={:.6f}".format(loss))

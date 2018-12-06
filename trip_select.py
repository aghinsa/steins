import numpy as np
import tensorflow as tf

def distance_mat(vecs):
    """
    input:vecs (batch,)
    return:(batch,batch)
        (i,j) in distances gives ||a-b||^2
    """
    vecs=tf.reshape(vecs,(-1,1))
    prod=tf.matmul(vecs,vecs.T)
    square=tf.linalg.dia(prod)
    
    #distance=(1,b)-2*(b,b)+(b,1)
    distances=tf.expand_dims(square,0)-2*prod+tf.expand_dims(square,1)
    
    return distances
def _positive_mask(labels):
    """
    labels:(b,1)
    return :mask(b,b) type:bool
         if i!=j and l[i]==l[j] mask =1
    """
    batch_size=tf.shape(labels)[0]
    ii=tf.cast(tf.eye(batch_size),bool)
    ij=tf.logical_not(ii)
    
    #finding (b,b) with labels same
    labels_same=tf.equal(tf.expand_dims(1,labels),tf.expand_dims(labels,1))
    #if i!=j and l[i]==l[j] mask =1
    mask=tf.logical_and(labels_same,ij)
    return mask
def _negative_mask(labels):
    """
    labels=(b,1)
    return :mask(b,b) type:bool
         if i!=j and l[i]!=l[j] mask =1
    """
    mask=tf.equal(tf.expand_dims(1,labels),tf.expand_dims(labels,1))
    mask=tf.logical_not(mask)
    return mask
    
def hard_k_negatives_postives(vecs,labels,k=1):
    """
    k=number of minimums/maximums to keep
    """
    distances=distance_mat(vecs)
    max_in_row=tf.reduce_max(distances,axis=1,keepDims=True)
    n_mask=_negative_mask(labels)
    #adding max to eac non valid to take min later
    distances_mod=distances*tf.to_float(tf.logical_not(n_mask))
    distances_mod=distances_mod+max_in_row*tf.to_float(tf.logical_not(n_mask))
    #hard_mins=tf.reduce_min(distances_mod,axis=1,keepDims=True)
    min_vals,_=tf.math.top_k(-distances_mod,k=k)
    hard_k_negativess=-min_vals
    ####################################
    
    p_mask=_positive_mask(labels)
    distances_mod=distances*tf.to_float(p_mask)
    hard_k_positives,_=tf.math.top_k(distances_mod,k=k )
    
    return hard_k_negatives,hard_k_positives
    #(b,1)
def hard_triplet_loss(vecs,labels,margin,k=1):
    hard_k_negatives,hard_k_positives=hard_k_negatives_postives(vecs,labels,k)
    #(batch,k)
    loss=0
    #loss=max(hp-hn+margin,0)
    for i in range(k):
        to_sub=tf.transpose(hard_k_negatives,[i%k,(i+1)%k,(i+2)%k])
        temp=tf.maximum(hard_k_positives-to_sub+margin,0)
        loss=loss+tf.reduce_mean(temp)
    return loss
        
    



    
    
    
    
    

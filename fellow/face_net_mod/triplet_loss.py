import numpy as np
import tensorflow as tf
# from sklearn.metrics.pairwise import euclidean_distances

def distance_mat(vecs):
    """
    input:vecs (batch,size)
    return:(batch,batch)
        (i,j) in distances gives ||a-b||^2
    """
    # distances=euclidean_distances(vecs,vecs,squared=True)
    distances=tf.square(tf.expand_dims(vecs,-1)-tf.transpose(vecs))
    distances=tf.reduce_sum(distances,1)
    return distances
    
def _positive_mask(labels):
    """
    labels:(b,1)
    return :mask(b,b) type:bool
         if i!=j and l[i]==l[j] mask =1
    """
    # labels=labels.reshape(-1)
    # labels=tf.reshape(labels,(-1))
    batch_size=tf.shape(labels)[0]
    ii=tf.cast(tf.eye(batch_size),bool)
    ij=tf.logical_not(ii)
    
    labels=tf.reshape(labels,[-1,1])
    n=tf.shape(labels)[0]
    labels_same=tf.tile(labels,(1,n))==tf.tile(tf.transpose(labels),(n,1))
    # labels_same=tf.linalg.set_diag(labels_same,0)
    #if i!=j and l[i]==l[j] mask =1
    mask=tf.logical_and(labels_same,ij)
    return mask
    
def _negative_mask(labels):
    """
    labels=(b,1)
    return :mask(b,b) type:bool
         if i!=j and l[i]!=l[j] mask =1
    """
    # labels=labels.reshape(-1)
    # labels=tf.reshape(labels,(-1))
    # mask=tf.equal(tf.expand_dims(labels,0),tf.expand_dims(labels,1
    labels=tf.reshape(labels,[-1,1])
    n=tf.shape(labels)[0]
    mask=tf.tile(labels,(1,n))==tf.tile(tf.transpose(labels),(n,1))
    # mask=tf.linalg.set_diag(labels_same,0)
    mask=tf.logical_not(mask)
    return mask
    
def hard_k_negatives_postives(vecs,labels,k=1):
    """
    k=number of minimums/maximums to keep
    """
    distances=distance_mat(vecs)
    max_in_row=tf.reduce_max(distances,axis=1,keepdims=True)
    n_mask=_negative_mask(labels)
    #adding max to eac non valid to take min later
    distances_mod=distances*tf.to_float(tf.logical_not(n_mask))
    distances_mod=distances_mod+max_in_row*tf.to_float(tf.logical_not(n_mask))
    #hard_mins=tf.reduce_min(distances_mod,axis=1,keepdims=True)
    min_vals,_=tf.math.top_k(-distances_mod,k=k)
    hard_k_negatives=-min_vals
    ####################################
    
    p_mask=_positive_mask(labels)
    distances_mod=distances*tf.to_float(p_mask)
    hard_k_positives,_=tf.math.top_k(distances_mod,k=k )
    
    return hard_k_negatives,hard_k_positives
    #(b,1)
def hard_triplet_loss(vecs,labels,margin=0.3,k=1):
    """
    vecs=embedding (batch,size_of_descp)
    labesl=(batch,1)
    k=number of hard_negatives/postives for an image
    
    return:triplet loss(float)
    """
    hard_k_negatives,hard_k_positives=hard_k_negatives_postives(vecs,labels,k)
    #(batch,k)
    loss=0
    #loss=max(hp-hn+margin,0)
    for i in range(k):
#         p=[i%k,(i+1)%k,(i+2)%k]
        p=[(i+j)%k for j in range(k)]
        l=len(p)
        perm=np.zeros(shape=(l,l))
        perm[np.arange(l),p]=1
        perm=tf.cast(perm,dtype=hard_k_negatives.dtype)
        to_sub=tf.matmul(hard_k_negatives,perm)
        
        temp=tf.maximum(hard_k_positives-to_sub+margin,0)
        temp=tf.reduce_sum(temp,axis=1)
        loss=loss+tf.reduce_mean(temp)
    return loss






    
    
    
    
    

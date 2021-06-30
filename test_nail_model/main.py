# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#test JTP classfication
import os
import caffe
import numpy as np
root='/home/cross_li/caffe-master'
deploy=root+'/models/vgg_finetune/deploy.prototxt'
caffe_model=root+'/models/vgg_finetune/vgg_finetune_iter_5000.caffemodel'

dir='/media/cross_li/94806D23806D0D54/JTP/ukbench/test_full/'
filelist=[]
filenames=os.listdir(dir)
for fn in filenames:
    fullfilename=os.path.join(dir,fn)
    filelist.append(fullfilename)
def Test(img):
    net=caffe.Net(deploy,caffe_model,caffe.TEST)
    transformer=caffe.io.Transformer({'data':net.blobs['data'].data.shape})
    transformer.set_transpose('data',(2,0,1))
    transformer.set_channel_swap('data',(2,1,0))
    transformer.set_raw_scale('data',255.0)

    net.blobs['data'].reshape(1,3,224,224)
    im=caffe.io.load_image(img)
    net.blobs['data'].data[...]=transformer.preprocess('data',im)

    out=net.forward()
    print(out['prob'].argmax())
for i in range(0,len(filelist)):
    img=filelist[i]
    Test(img)
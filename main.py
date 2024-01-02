# -*- coding: utf-8 -*-
"""
FBP task are conduct on BLS_Regression
Created on Wed Oct 10 04:37:31 2024
@author: Xiaoshan Xie, e-mail: xiaoshanxie.xsx@gmail.com
This code is the first version of BLS Python. 
If you have any questions about the code or find any bugs
   or errors during use, please feel free to contact me.
If you have any questions about the original paper, 
   please contact the authors of related paper.
"""

# load 
import numpy as np
import scipy.io as scio
import cv2
import sys
import os
from BLS_Regression import bls_regression

# image_path
image_folder = "./datasets/SCUT-FBP5500_v2/Images"
# image_folder = "./datasets/SCUT-FBP/Images"
# image_folder = "./datasets/MEBeauty"

def getDatanew(filePath, resize_format=(224, 224), colorType=cv2.IMREAD_COLOR, resize_interpolation=cv2.INTER_LANCZOS4, needGenImg=False): 
    tmpData = []
    tmpLabel = []
    with open(filePath, 'r', encoding='utf-8') as txtData:
        lines = txtData.readlines()
        for line in lines:
            file, label = line.strip().split() 
            label=float(label) # string to float
            tmpLabel.append(label)
            # fileName = file
            fileName = os.path.join(image_folder, file)
            img = cv2.imread(fileName, 1)
            img_formated = cv2.resize(img, resize_format, interpolation=resize_interpolation)
            img_formated = np.expand_dims(img_formated, axis=0)
            img_flat = img_formated.ravel()
            tmpData.append(img_flat)
    return np.double(tmpData), np.double(tmpLabel) # return samples and labels

# The parameters of BLS
NumFea = 6
NumWin = 5
NumEnhan = 41
s = 0.8
C = 2**-30

#  dataset path
# SCUT-FBP5500 dataset
filePath_train = r'./datasets/SCUT-FBP5500_v2/train.txt'
filePath_test = r'./datasets/SCUT-FBP5500_v2/test.txt'

# MEBeauty dataset
# filePath_train = r'./datasets/MEBeauty/train.txt'
# filePath_test = r'./datasets/MEBeauty/test.txt'

# SCUT-FBP dataset
# filePath_train = r'./datasets/SCUT-FBP/train.txt'
# filePath_test = r'./datasets/SCUT-FBP/test.txt'

# Load data
traindata, trainlabel = getDatanew(filePath_train)
testdata, testlabel = getDatanew(filePath_test)

# save data
# np.save('./data/traindata.npy', traindata)
# np.save('./data/trainlabel.npy', trainlabel)
# np.save('./data/testdata.npy', testdata)
# np.save('./data/testlabel.npy', testlabel)

# load saved data
# traindata = np.load("./data/traindata.npy",encoding = "bytes")
# trainlabel = np.load("./data/trainlabel.npy",encoding = "bytes")
# testdata = np.load("./data/testdata.npy",encoding = "bytes")
# testlabel = np.load("./data/testlabel.npy",encoding = "bytes")

# train and test
bls_regression(traindata,trainlabel,testdata,testlabel,s,C,NumFea,NumWin,NumEnhan)


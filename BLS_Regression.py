# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 03:18:22 2018
@author: XiaoshanXie e-mail:xiaoshanxie.xsx@gmail.com
This code is the first version of BLS Python. 
If you have any questions about the code or find any bugs
   or errors during use, please feel free to contact me.
If you have any questions about the original paper, 
   please contact the authors of related paper.
"""
import numpy as np
from sklearn import preprocessing
from numpy import random
import time
from sklearn.metrics import mean_squared_error, mean_absolute_error

'''
激活函数
'''
def relu(x):
    return np.maximum(0, x)

def leaky_relu(x, alpha=0.01):
    return np.maximum(alpha * x, x)

def pinv(A,reg):
    return np.mat(reg*np.eye(A.shape[1])+A.T.dot(A)).I.dot(A.T)

'''
参数压缩
'''
def shrinkage(a,b):
    z = np.maximum(a - b, 0) - np.maximum( -a - b, 0)
    return z
'''
参数稀疏化
'''
def sparse_bls(A,b):
    lam = 0.001
    itrs = 50
    AA = np.dot(A.T,A)   
    m = A.shape[1]
    n = b.shape[1]
    wk = np.zeros([m,n],dtype = 'double')
    ok = np.zeros([m,n],dtype = 'double')
    uk = np.zeros([m,n],dtype = 'double')
    L1 = np.mat(AA + np.eye(m)).I
    L2 = np.dot(np.dot(L1,A.T),b)
    for i in range(itrs):
        tempc = ok - uk
        ck =  L2 + np.dot(L1,tempc)
        ok = shrinkage(ck + uk, lam)
        uk += ck - ok
        wk = ok
    return wk

def bls_regression(train_x,train_y,test_x,test_y,s,C,NumFea,NumWin,NumEnhan):  
    u = 0
    WF = list()
    for i in range(NumWin):
        random.seed(i+u)
        WeightFea=2*random.randn(train_x.shape[1]+1,NumFea)-1
        WF.append(WeightFea)
#    random.seed(100)
    WeightEnhan=2*random.randn(NumWin*NumFea+1,NumEnhan)-1
    time_start = time.time()
    H1 = np.hstack([train_x, 0.1 * np.ones([train_x.shape[0],1])])
    y = np.zeros([train_x.shape[0],NumWin*NumFea])
    WFSparse = list()
    distOfMaxAndMin = np.zeros(NumWin)
    meanOfEachWindow = np.zeros(NumWin)
    for i in range(NumWin):
        WeightFea = WF[i]
        A1 = H1.dot(WeightFea)        
        scaler1 = preprocessing.MinMaxScaler(feature_range=(-1, 1)).fit(A1)
        A1 = scaler1.transform(A1)
        WeightFeaSparse  = sparse_bls(A1,H1).T
        WFSparse.append(WeightFeaSparse)
    
        T1 = H1.dot(WeightFeaSparse)
        # T1 = relu(T1)
        meanOfEachWindow[i] = T1.mean()
        distOfMaxAndMin[i] = T1.max() - T1.min()
        T1 = (T1 - meanOfEachWindow[i])/distOfMaxAndMin[i] 
        y[:,NumFea*i:NumFea*(i+1)] = T1

    H2 = np.hstack([y,0.1 * np.ones([y.shape[0],1])])
    T2 = H2.dot(WeightEnhan)
    T2 = leaky_relu(T2)
    T3 = np.hstack([y,T2])
    WeightTop = pinv(T3,C).dot(train_y)
    WeightTop = np.transpose(WeightTop) # 转置
    Training_time = time.time()- time_start
    print('Training has been finished!')
    print('The Total Training Time is : ', round(Training_time,6), ' s')
    NetoutTrain = T3.dot(WeightTop)

    # Calculate the training accuracy
    train_y = np.array(train_y)
    NetoutTrain = np.array(np.ravel(NetoutTrain))
    train_pc = np.mean(np.corrcoef(train_y, NetoutTrain))
    train_mae = np.mean(np.abs(train_y - NetoutTrain))
    train_rmse = np.sqrt(np.mean(np.square(train_y - NetoutTrain)))
    print('Training PC is : ', train_pc)
    print('Training MAE is : ', train_mae)
    print('Training RMSE is : ', train_rmse)
    time_start = time.time()

    HH1 = np.hstack([test_x, 0.1 * np.ones([test_x.shape[0],1])])
    yy1=np.zeros([test_x.shape[0],NumWin*NumFea])
    for i in range(NumWin):
        WeightFeaSparse = WFSparse[i]
        TT1 = HH1.dot(WeightFeaSparse)
        # TT1 = relu(TT1)
        TT1  = (TT1 - meanOfEachWindow[i])/distOfMaxAndMin[i]   
        yy1[:,NumFea*i:NumFea*(i+1)] = TT1

    HH2 = np.hstack([yy1, 0.1 * np.ones([yy1.shape[0],1])])
    TT2 = HH2.dot( WeightEnhan)
    TT2 = leaky_relu(TT2)
    TT3 = np.hstack([yy1,TT2])
    NetoutTest = TT3.dot(WeightTop)

    test_y = np.array(test_y)
    NetoutTest = np.array(np.ravel(NetoutTest))
    test_pc = np.mean(np.corrcoef(test_y, NetoutTest))
    test_mae = np.mean(np.abs(test_y - NetoutTest))
    test_rmse = np.sqrt(np.mean(np.square(test_y - NetoutTest)))

    # Calculate the testing accuracy
    Testing_time = time.time() - time_start
    print('Testing has been finished!')
    print('The Total Testing Time is : ', round(Testing_time,6), ' s' )
    print('Testing PC is : ', test_pc) 
    print('Testing MAE is : ', test_mae) 
    print('Testing RMSE is : ', test_rmse) 

    return train_mae, train_rmse, Testing_time, test_mae, test_rmse, Training_time

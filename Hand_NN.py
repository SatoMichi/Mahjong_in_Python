# REFERENCE LIST:　やさしく学ぶディープラーニングがわかる数学のきほん
import numpy as np
import math

# Prepare Data
# X is the input data which represent hand with 13 pai
# since input have to be int vector with len 13, all the mahjong pai have to be represented as int
# Y should be supervised answer for each data

# standardize
mu = XI.mean(axis=0)
sigma = XI.std(axis=0)

def standardize(X):
    return (X-mu)/sigma

X = standardize(XI)
print("Data Prepared.")
# since our data is not very complicated, standardize coud be skiped

# NN structure 13->9->3->1
W1 = np.random.randn(9,13)
b1 = np.random.randn(9)
W2 = np.random.randn(3,9)
b2 = np.random.randn(3)
W3 = np.random.randn(1,3)
b3 = np.random.randn(1)

# NN function
# use sigmoid
def sigmoid(x):
    return 1 /(1 + np.exp(-x))

def forward(X0):
    Z1 = np.dot(X0,W1.T) + b1
    X1 = sigmoid(Z1)
    Z2 = np.dot(X1,W2.T) + b2
    X2 = sigmoid(Z2)
    Z3 = np.dot(X2,W3.T) + b3
    X3 = sigmoid(Z3)
    return (Z1,X1,Z2,X2,Z3,X3)

# differenciated function for backward
def dsigmoid(x):
    return (1-sigmoid(x))*sigmoid(x)

def deltaOut(Z,Y):
    return (sigmoid(Z)-Y)*dsigmoid(Z)

def deltaHid(Z,D,W):
    return dsigmoid(Z)*np.dot(D,W)

def backward(Y,Z3,Z2,Z1):
    D3 = deltaOut(Z3,Y)
    D2 = deltaHid(Z2,D3,W3)
    D1 = deltaHid(Z1,D2,W2)
    return (D1,D2,D3)

# Leraning
def dweight(D,X):
    return np.dot(D.T,X)

def dbias(D):
    return D.sum(axis=0)

def update(D3,X2,D2,X1,D1,X0):
    eta = 0.001
    global W3,W2,W1,b3,b2,b1
    W3 = W3 - eta*dweight(D3,X2)
    W2 = W2 - eta*dweight(D2,X1)
    W1 = W1 - eta*dweight(D1,X0)
    b3 = b3 - eta * dbias(D3)
    b2 = b2 - eta * dbias(D2)
    b1 = b1 - eta * dbias(D1)

def train(X,Y):
    Z1,X1,Z2,X2,Z3,X3 = forward(X)
    D1,D2,D3 = backward(Y,Z3,Z2,Z1)
    update(D3,X2,D2,X1,D1,X)

def predict(X):
    return forward(X)[-1]

def E(Y,X):
    return 0.5 * ((Y - predict(X))**2).sum()

# main()
epoch = 30000
batch = 100

for epo in range(1,epoch+1):
    p = np.random.permutation(len(X))
    for i in range(math.ceil(len(X)/batch)):
        indice = p[i*batch:(i+1)*batch]
        X0 = X[indice]
        Y0 = Y[indice]
        train(X0,Y0)
    # Log
    if epo % 1000 == 0:
        print("Error = ",E(Y,X)," epoch = ",epo)

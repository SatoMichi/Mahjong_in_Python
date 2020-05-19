import numpy as np
import pandas as pd


def toArray(scores):
    scores = scores.split("/")
    scores = list(map(lambda x: None if x=="None" else int(x), scores))
    return np.array(scores)


label = ["20","25","30","40","50","60","70","80","90","100","110"]

# load table for eastPlayer
east = pd.read_csv("eastPlayerScore.csv", header=0)
npy = np.zeros([13,11,2])

for j,l in enumerate(label):
    for i,elem in enumerate(east[l]):
        elem = toArray(elem)
        npy[i,j,0] = elem[0]
        npy[i,j,1] = elem[1]

np.save("eastPlayerScore",npy)

# load table for Non-eastPlayer
east = pd.read_csv("nonEastPlayerScore.csv", header=0)
npy = np.zeros([13,11,3])

for j,l in enumerate(label):
    for i,elem in enumerate(east[l]):
        elem = toArray(elem)
        npy[i,j,0] = elem[0]
        npy[i,j,1] = elem[1]
        npy[i,j,2] = elem[2]

np.save("nonEastPlayerScore",npy)
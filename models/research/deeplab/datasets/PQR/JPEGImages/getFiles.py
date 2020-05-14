import os
from os import listdir
from os.path import isfile, join

cwd = os.getcwd()
files = listdir("/Users/chen/Downloads/tfdeeplab/deeplab/models/research/deeplab/datasets/PQR/JPEGImages")
for f in files:
    print(f.replace(".jpg",""))

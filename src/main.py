# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 23:27:16 2019

@author: Kenng
@email: kenng7183@gmail.com
@github: kennethng555
"""
import os
import psutil
import time

import pandas as pd
# from matplotlib import pyplot
# from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import sys

from Tree import Tree
from Node import Node
from FPgrowth import FP_growth
from Preprocessing import *


if __name__ == '__main__':
    f = open("output.txt", "w+")
    process = psutil.Process(os.getpid())
    start_time = time.time()

    ## uncomment to export events to a text file
    # original = sys.stdout
    # sys.stdout = open('events.txt', 'w')

    file = "data/Test.csv"
    print('input file: ', file)
    df = pd.read_csv(file)
    threshold = 2
    # NumericalDims = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    # NoPartitions = 2

    print('Attempting to discretize the imported dataset...')
    # df = discretize(df, NumericalDims, NoPartitions)
    print('Proceeding to FP Growth algorithm...')

    df = decode(df)
    countdict = gen_freq(df, threshold)
    sortorder = sorted(countdict.items(), key=lambda k: (k[1], k[0]), reverse=True)
    ordered = df.values.tolist()
    ordered = order_itemset(ordered, sortorder)
    root = Node(data=[])
    sortorder = sorted(countdict.items(), key=lambda k: (k[1], k[0]))
    countdict = convert_dict(countdict, sortorder)
    fptree = Tree(root, data=countdict)
    fptree.generate(ordered)
    a = []
    FP_growth(fptree, a, threshold)

    print("--- %s seconds ---" % (time.time() - start_time))
    print("Total Bytes Used: ", end='')
    print(process.memory_info().rss)

    f.close()
    # sys.stdout = original

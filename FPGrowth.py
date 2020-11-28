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
import numpy as np
import math
#from matplotlib import pyplot
#from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import sys

f= open("output.txt","w+")
process = psutil.Process(os.getpid())
start_time = time.time()

class Node(object):
    def __init__(self, data=None, count=0, left_node=None, right_node=None, parent=None, link=None, uplink=None):
        self.data = data
        self.count = count
        self.left_node = left_node
        self.right_node = right_node
        self.parent = parent
        self.link = link
        self.uplink = uplink

    def get_data(self):
        return self.data

    def get_count(self):
        return self.count

    def get_left(self):
        return self.left_node

    def get_right(self):
        return self.right_node
    
    def get_parent(self):
        return self.parent

    def set_count(self, new_count):
        self.count = new_count

    def set_left(self, new_left):
        self.left_node = new_left

    def set_right(self, new_right):
        self.right_node = new_right
        
    def set_parent(self, new_parent):
        self.parent = new_parent

class Tree(object):
    def __init__(self, root=None, data=None):
        self.root = root
        self.head = root
        self.latest = data
        
    def insert_left(self, node):
        self.head.set_left(node)
        self.head = node

    def insert_right(self, node):
        self.head.set_right(node)
        self.head = node
        
    def insert_link(self, key, node):
        node.uplink = self.latest[key]
        self.latest[key].link = node
        self.latest[key] = node
        
    def reset_links(self):
        for key in self.latest.keys():
            while self.latest[key].uplink is not None:
                self.latest[key] = self.latest[key].uplink
        
    # generate the tree from the original database
    def generate(self, ordered):
        for i in range(len(ordered)):
            for j in range(len(ordered[i])):
                if(self.head.get_left() == None):
                    new_left = Node(data=ordered[i][j], count=1, parent = self.head)
                    self.insert_left(new_left)
                    self.insert_link(ordered[i][j], self.head)
                else:
                    self.head = self.head.get_left()
                    if self.head.data == ordered[i][j]:
                        self.head.set_count(self.head.get_count() + 1)
                    else:
                        while self.head.get_right() is not None and self.head.get_data() != ordered[i][j]:
                            self.head = self.head.get_right()
                        if self.head.get_right() is None and self.head.get_data() != ordered[i][j]:
                            new_right = Node(data=ordered[i][j], count=1, parent = self.head.get_parent())
                            self.insert_right(new_right)
                            self.insert_link(ordered[i][j], self.head)
                        elif self.head.get_data() == ordered[i][j]:
                            self.head.set_count(self.head.get_count() + 1)
            self.head = self.root
        self.reset_links()
    
    # generate sub tree based on the path with the support of the path
    def generatesub(self, paths, support):
        for i in range(len(paths)):
            for j in range(len(paths[i])):
                if paths[i][j] in self.latest:
                    if self.head.get_left() is not None:
                        self.head = self.head.get_left()
                        if self.head.data == paths[i][j]:
                            self.head.count = self.head.count + support[i]
                        else:
                            while self.head.get_right() is not None and self.head.get_data() != paths[i][j]:
                                self.head = self.head.get_right()
                            if self.head.get_right() is None and self.head.get_data() != paths[i][j]:
                                new_right = Node(paths[i][j], count=support[i], parent = self.head.get_parent())
                                self.insert_right(new_right)
                                self.insert_link(paths[i][j], self.head)
                            elif self.head.get_data() == paths[i][j]:
                                self.head.set_count(self.head.get_count() + support[i])
                    else:
                        new_left = Node(data=paths[i][j], count=support[i], parent = self.head)
                        self.insert_left(new_left)
                        self.insert_link(paths[i][j], self.head)
            self.head = self.root
        self.reset_links()

# FP Growth
def FP_growth(tree, a, min_sup):
    # find if there is only 1 path
    while tree.head is not None and tree.head.get_right() is None:
        tree.head = tree.head.get_left()
    result = []
    
    if tree.head is None:                     # if there is one path, print all combinations of all elements
        tree.head = tree.root
        print("Combination: ")
        print("----------",a,"---------")
        tree.head = tree.head.get_left()
        while tree.head is not None:
            sup = tree.head.count
            s = len(result)
            result.extend(result)
            for i in range(s,len(result)):
                if isinstance(result[i], str):
                    result[i] = [result[i]] + [tree.head.get_data()]
                else:
                    result[i] = result[i] + [tree.head.get_data()]
            result.append(tree.head.get_data())
            tree.head = tree.head.get_left()
            
        for i in range(len(result)):
            if isinstance(result[i], str):
                result[i] = [result[i]] + [', '.join(a)]
            else:
                result[i] = result[i] + [', '.join(a)]
            print(', '.join(result[i]), ": ", sup)
        print('\n')
    else:                                     # if there is more than one path use the dictionary to look up
        condpatbase = dict()                  # set the leaves and form a new tree based on the paths to the
        condfreqpat = dict()                  # node
        for key in tree.latest.keys():
            if tree.latest[key].count >= min_sup:
                current = tree.latest[key].link
                paths = []
                common = []
                supports = []
                subcondpatbase = dict()
                while current is not None:
                    path = []
                    start = current
                    print(key, end='\t')
                    current = current.get_parent()
                    while current.data != []:
                        if current.data in subcondpatbase:
                            subcondpatbase[current.data].count = subcondpatbase[current.data].count + start.count
                        else:
                            subcondpatbase[current.data] = Node(current.data, start.count)
                        path.insert(0, current.data)
                        print(current.get_data(), end=' ')
                        current = current.get_parent()
                    current = start
                    if path != []:
                        paths.append(path)
                        supports.append(current.count)
                        print(current.count)
                    else:
                        print('\n')
                    current = current.link
                
                for subkey in list(subcondpatbase.keys()):
                    if subcondpatbase[subkey].count < min_sup:
                        del subcondpatbase[subkey]
                
                if subcondpatbase != {}:                        # if the conditional path base is not empty, 
                    print()                                     # generate the tree and pass the tree to
                    root = Node(data=[])                        # recursive call to FP Growth
                    btree = Tree(root, subcondpatbase)
                    if paths != []:
                        btree.generatesub(paths, supports)
                        condpatbase[key] = (paths, supports)
                        a.append(key)
                        FP_growth(btree, a, min_sup)
                        condfreqpat[key] = (common, min_sup)
                        a.pop()
                else:
                    print("Combination: ")
                    print("----------",a+[key],"---------")
                    print(', '.join(a+[key]), ": ", tree.latest[key].count)
                    print('\n')
        print("------------------------------------------------")
        print("--------------------New Path--------------------")
        print("------------------------------------------------")

# generates frequency
def gen_freq(df, threshold=0):        
    un = dict()
    for i in range(len(df.columns)):
        unique = np.unique(df.iloc[:, i])
        for j in range(len(unique)):
            if threshold <= len(df.iloc[:, i][df.iloc[:, i] == unique[j]]):
                un[unique[j]] = len(df.iloc[:, i][df.iloc[:, i] == unique[j]])
    return un

def order_itemset(dflist, sortorder):
    ordered = [[]] * len(dflist)
    for i in range(len(dflist)):
        ordered[i] = ([y for tuple in sortorder for y in dflist[i] if y == tuple[0]])
    return ordered

# turns integer categories into strings with labels
def decode(df):
    separator = '_'
    separator2 = ''
    for i in range(len(df.columns)):
        label = separator2.join([chr(97+math.floor(i/26)) * (math.floor(i/26)), chr(97+(i%26))])
        f.write(label)
        f.write(' - ')
        f.write(df.columns[i])
        f.write('\n')
        for j in range(len(df)):
            df.iloc[j,i] = separator.join([label, str(int(df.iloc[j,i]))])
    return df

# converts dictionary with frequency counts to nodes with name and frequency count
def convert_dict(countdict, sortorder):
    for i in range(len(sortorder)):
        countdict[sortorder[i][0]] = Node(data=sortorder[i][0], count=sortorder[i][1])
    return countdict

# splits the numerical dataset into labels for each bin with an equal amount of elements in each bin
def discretize(df, NumericalDims, NoPartitions):
    ### Equilength Binning
    Xmax = [0]*len(df.columns)
    Xmin = [0]*len(df.columns)
    dX   = [0]*len(df.columns)
    # Scan 1:
        # Determine the max and min of each column
    for j in NumericalDims:
            ColMax = df.iloc[0,j];
            ColMin = df.iloc[0,j];
            for i in range(len(df)):
                if df.iloc[i,j] < ColMin:
                    ColMin = df.iloc[i,j]
                if df.iloc[i,j] > ColMax:
                    ColMax = df.iloc[i,j]
            Xmax[j] = ColMax
            Xmin[j] = ColMin
            dX[j] = (Xmax[j] - Xmin[j]) / (NoPartitions-1)
    # Scan 2: 
        # Replace numerical data with it's discretized form (represented as an integer)
    for j in NumericalDims:
            for i in range(len(df)):
                df.iloc[i,j] = math.floor((df.iloc[i,j]-Xmin[j])/dX[j])
    return df.astype(int)

## uncomment to export events to a text file
#original = sys.stdout
#sys.stdout = open('events.txt', 'w')

file = "C:/Users/Kenng/Downloads/Test.csv"
print('input file: ', file)
df = pd.read_csv(file)
threshold = 2
#NumericalDims = [1,2,3,4,5,6,7,8,9,10,11,12,13]
#NoPartitions = 2

print('Attempting to discretize the imported dataset...')
#df = discretize(df, NumericalDims, NoPartitions)
print('Proceeding to FP Growth algorithm...')

df = decode(df)
countdict = gen_freq(df, threshold)
sortorder = sorted(countdict.items(), key=lambda k:(k[1],k[0]), reverse=True)
ordered = df.values.tolist()
ordered = order_itemset(ordered, sortorder)
root = Node(data=[])
sortorder = sorted(countdict.items(), key=lambda k:(k[1],k[0]))
countdict = convert_dict(countdict, sortorder)
fptree = Tree(root, data=countdict)
fptree.generate(ordered)
a = []
FP_growth(fptree, a, threshold)

print("--- %s seconds ---" % (time.time() - start_time))
print("Total Bytes Used: ", end = '')
print(process.memory_info().rss)

f.close()
#sys.stdout = original
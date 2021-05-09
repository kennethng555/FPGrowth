import math
import numpy as np
from Node import Node


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
    f = open("output.txt", "w+")
    separator = '_'
    separator2 = ''
    for i in range(len(df.columns)):
        label = separator2.join([chr(97 + math.floor(i / 26)) * (math.floor(i / 26)), chr(97 + (i % 26))])
        f.write(label)
        f.write(' - ')
        f.write(df.columns[i])
        f.write('\n')
        for j in range(len(df)):
            df.iloc[j, i] = separator.join([label, str(int(df.iloc[j, i]))])
    f.close()
    return df


# converts dictionary with frequency counts to nodes with name and frequency count
def convert_dict(countdict, sortorder):
    for i in range(len(sortorder)):
        countdict[sortorder[i][0]] = Node(data=sortorder[i][0], count=sortorder[i][1])
    return countdict


# splits the numerical dataset into labels for each bin with an equal amount of elements in each bin
def discretize(df, NumericalDims, NoPartitions):
    ### Equilength Binning
    Xmax = [0] * len(df.columns)
    Xmin = [0] * len(df.columns)
    dX = [0] * len(df.columns)
    # Scan 1:
    # Determine the max and min of each column
    for j in NumericalDims:
        ColMax = df.iloc[0, j];
        ColMin = df.iloc[0, j];
        for i in range(len(df)):
            if df.iloc[i, j] < ColMin:
                ColMin = df.iloc[i, j]
            if df.iloc[i, j] > ColMax:
                ColMax = df.iloc[i, j]
        Xmax[j] = ColMax
        Xmin[j] = ColMin
        dX[j] = (Xmax[j] - Xmin[j]) / (NoPartitions - 1)
    # Scan 2:
    # Replace numerical data with it's discretized form (represented as an integer)
    for j in NumericalDims:
        for i in range(len(df)):
            df.iloc[i, j] = math.floor((df.iloc[i, j] - Xmin[j]) / dX[j])
    return df.astype(int)
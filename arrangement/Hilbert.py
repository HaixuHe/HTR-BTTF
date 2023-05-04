import math
import numpy as np
from utils import *
from tqdm import tqdm

L = [[0, 0]]


def move(l, a):
    k = l[-1]
    if abs(a % 4) == 1:
        l.append([k[0], k[1] + 1])
    elif abs(a % 4) == 3:
        l.append([k[0], k[1] - 1])
    elif abs(a % 4) == 0:
        l.append([k[0] + 1, k[1]])
    elif abs(a % 4) == 2:
        l.append([k[0] - 1, k[1]])


def hl(n, s):
    if n == 0:
        pass
    if n > 0:
        s += 1
        hr(n - 1, s)
        move(L, s)
        s -= 1
        hl(n - 1, s)
        move(L, s)
        hl(n - 1, s)
        s -= 1
        move(L, s)
        hr(n - 1, s)
        s += 1


def hr(n, s):
    if n == 0:
        pass
    if n > 0:
        s -= 1
        hl(n - 1, s)
        move(L, s)
        s += 1
        hr(n - 1, s)
        move(L, s)
        hr(n - 1, s)
        s += 1
        move(L, s)
        hl(n - 1, s)
        s -= 1


def _hibert(n):
    hl(n, 0)


def Hilbert_tensor_rearrangement(d):  # 使用希尔伯特重构
    data = d.copy()
    _hibert(8)
    z, x, y = data.shape
    T = 46
    new_data = np.zeros([T, int(z / T), x * y])
    f = []
    for t in tqdm(range(T)):
        xx = 0
        for zz in range(z):
            if zz % T == t:
                s = []
                for i in L:
                    if 52 < i[0] < 203 and 52 < i[1] < 203:
                        s.append(data[zz][i[0] - 53][i[1] - 53])
                        if t == 45:
                            f.append([i[0] - 53, i[1] - 53])

                s = np.array(s)
                new_data[t][xx] = s
                xx += 1
    return new_data, f


def reshape_Hilbert(im_data, f):  # 恢复张量维度
    im_data1 = im_data.transpose()
    new_data = np.zeros([138, 150, 150])
    c = 0
    for i in range(im_data1.shape[1]):
        for j in range(im_data1.shape[2]):
            temp = np.zeros([150, 150])
            for m, value in zip(f, im_data1[:, i, j]):
                temp[m[0], m[1]] = value
            new_data[c] = temp
            c += 1
    return new_data

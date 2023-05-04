'''
Descripttion: 
Author: Haixu He
Date: 2022-01-10 22:36:12
'''
"""
为了实现快速的计算，试一下将张量翻转
"""
import numpy as np


def Block(sparse_tensor, flip):  # 张量分块，flip为分块个数
    dim1, dim2, dim3 = sparse_tensor.shape
    if sparse_tensor.shape[-1] % flip == 0:  # 如果没办法整除
        x = np.linspace(0, dim3 - 1, dim3).astype('int')
        temp = np.zeros([flip, dim1, dim2, int(dim3 / flip)])
        for i in range(flip):
            x1 = x[x % flip == 0] + i
            temp[i] = sparse_tensor[:, :, x1]
        return temp
    else:
        raise Exception("没办法整除！")


def Combine_Block(tensor):  # 将多个张量块合并
    temp = tensor[0]
    for i in tensor[1:]:
        temp = np.concatenate((temp, i), axis=1)
    return temp


def flip(sparse_tensor, flip):
    return Combine_Block(Block(sparse_tensor, flip))


def reshape_tensor(tensor, sparse_tensor_raw, flip):
    tensor = tensor.transpose()
    Years = sparse_tensor_raw.shape[1]
    temp = np.zeros_like(sparse_tensor_raw)
    c = 0
    for i in range(tensor.shape[-1]):
        for j in range(flip):
            temp[:, :, c] = tensor[:, Years * j:Years * j + Years, i]
            c += 1
    return temp


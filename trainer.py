import random
import os
from utils import *
import arrangement.Hilbert
import arrangement.Tensor_flip
from models.H_BTTF import train_model
import numpy as np

miss_rate = [0.1, 0.2, 0.4, 0.6, 0.8]


def original_BTTF(arges):  # 不使用张量重构

    sparse_tensor_raw, im_geotrans, im_proj = readGeoTIFF(arges.tif_path)

    tensor_hat, burn, time = train_model(sparse_tensor_raw, arges.burn_iter, arges.gibbs_iter,
                                                                arges.rank, arges.scale, arges.early_stop, arges.decline_rate)

    tensor_hat = tensor_hat.transpose()
    name = 'Original_BTTF_time_{}.tif'.format(time)
    CreateGeoTiff(os.path.join(arges.tif_out_path, name), tensor_hat, im_geotrans, im_proj)
    print('{} 保存成功！'.format(name))



def Hilbert_BTTF(arges):  # 使用Hilbert重构

    sparse_tensor_raw, im_geotrans, im_proj = readGeoTIFF(arges.tif_path)
    sparse_tensor_H, index_list = arrangement.Hilbert.Hilbert_tensor_rearrangement(sparse_tensor_raw)  # 使用Hilbert重构
    sparse_tensor = arrangement.Tensor_flip.flip(sparse_tensor_H, arges.block)  # 张量分块

    tensor_hat, burn, time = train_model(sparse_tensor, arges.burn_iter, arges.gibbs_iter,
                                                                arges.rank, arges.scale, arges.early_stop, arges.decline_rate)

    tensor_hat = arrangement.Tensor_flip.reshape_tensor(tensor_hat, sparse_tensor_H, arges.block)  #分块恢复
    tensor_hat = arrangement.Hilbert.reshape_Hilbert(tensor_hat, index_list)
    name = 'HTR_BTTF time_{}.tif'.format(time)
    CreateGeoTiff(os.path.join(arges.tif_out_path, name), tensor_hat, im_geotrans, im_proj)
    print('{} 保存成功！'.format(name))


def testModels(arges):
    print('开始运行...')
    if not os.path.exists(arges.tif_out_path):
        os.makedirs(arges.tif_out_path)

    original_BTTF(arges)   # 原始的BTTF模型
    Hilbert_BTTF(arges)    # HTR-BTTF模型

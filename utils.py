"""
基础函数：tif文件的读写
"""
import numpy as np
import random
from numpy.random import multivariate_normal as mvnrnd
from numpy.linalg import inv as inv
from osgeo import gdal, osr
import matplotlib.pylab as plt
import pandas as pd
import os


def CreateGeoTiff(outRaster, image, geo_transform, projection):
    no_bands = 0
    rows = 0
    cols = 0

    driver = gdal.GetDriverByName('GTiff')
    # print("元组长度:", len(image.shape))
    if len(image.shape) == 2:
        no_bands = 1
        rows, cols = image.shape
    elif len(image.shape) == 3:
        no_bands, rows, cols = image.shape

    # print("波段：", no_bands, "Rows:", rows, "Cols:", cols)
    # DataSet = driver.Create(outRaster, cols, rows, no_bands, gdal.GDT_Byte)
    DataSet = driver.Create(outRaster, cols, rows, no_bands, gdal.GDT_Float32)
    # # follow code is adding GeoTranform and Projection
    DataSet.SetGeoTransform(geo_transform)
    DataSet.SetProjection(projection)

    if no_bands == 1:
        DataSet.GetRasterBand(1).WriteArray(image)  # 写入数组数据
    else:
        for i in range(no_bands):
            DataSet.GetRasterBand(i + 1).WriteArray(image[i])
    del DataSet


def readGeoTIFF(fileName):
    dataset = gdal.Open(fileName)
    if dataset == None:
        print(fileName + "文件无法打开")

    im_width = dataset.RasterXSize  # 栅格矩阵的列数
    im_height = dataset.RasterYSize  # 栅格矩阵的行数
    im_data = dataset.ReadAsArray(0, 0, im_width, im_height)  # 获取数据

    im_geotrans = dataset.GetGeoTransform()  # 获取仿射矩阵信息
    im_proj = dataset.GetProjection()  # 获取投影信息
    return im_data, im_geotrans, im_proj

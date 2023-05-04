'''
Descripttion: 测试接口
Author: Haixu He
Date: 2022-01-10 22:39:39
'''

from argparse import ArgumentParser
import trainer


if __name__ == '__main__':
    # ------------
    # args
    # ------------
    parser = ArgumentParser()

    # path
    parser.add_argument('--tif_path', type=str, default='DemoData/data.tif')   # 待插补文件
    parser.add_argument('--tif_out_path', type=str, default='DemoData/output')  # 插补后tif文件输出路径

    # model
    parser.add_argument('--scale', default=0.02, type=float)  # 是否乘以scale
    parser.add_argument('--burn_iter', default=1200, type=int)  # burn次数
    parser.add_argument('--gibbs_iter', default=200, type=int)  # Gibbs采样次数
    parser.add_argument('--rank', default=30, type=int)  # 秩
    parser.add_argument('--block', default=1, type=int)  # 分块个数-restack

    # early_stop
    parser.add_argument('--early_stop', default=True, type=bool)  # 是否early_stop
    parser.add_argument('--decline_rate', default=0.01, type=float)  # 100次内rmse的下降水平

    args, unknow = parser.parse_known_args()

    trainer.testModels(args)  # 插值



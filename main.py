# -*-coding:utf-8-*-
# @Author: lizhaoyang
# @Date: 2024-09-03 15:38
# @file: main.py
# @software: PyCharm

import os, sys
import pandas as pd

from concept_drift_detector.concept_drift_detector import ConceptDriftDetector

sys.path.append("F:/quantchina/my_code/concept_drift_detect_tool/concept_drift_detector/concept_drift")

def main(data):
    '''
    主函数：完成数据输入，数据流获取，概念漂移检测及结果输出
    '''
    detector = ConceptDriftDetector()
    detector.concept_drift_detect(data)
    detector.concept_drift_analyse()
    detector.concept_drift_visualize()


if __name__ == "__main__":
    main(data = None)

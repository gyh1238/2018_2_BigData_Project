# -*- coding: utf-8 -*-
from mapAPI.v2.filter_v2 import JibunFilter
import pandas as pd

if __name__ == '__main__':
    j = JibunFilter()  # Jibun Filtering Object

    # str type data
    data_a = '서울특별시 종로구 명륜1가 36-27번지'

    # list type data
    data_b = ['서울특별시 종로구 명륜1가 36-27번지', '서울특별시 종로구 명륜1가 36-23번지']

    # Series type data
    data_c = pd.Series(data_b)

    # Output type: ndarray
    result_a = j(data_a)
    result_b = j(data_b)
    result_c = j(data_c)

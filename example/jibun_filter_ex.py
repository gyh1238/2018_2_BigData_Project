# -*- coding: utf-8 -*-
from mapAPI.filter import jibun_filter
import pandas as pd

if __name__ == '__main__':
    # 전체데이터_서울_원본.xlsx 불러오기
    raw_data = pd.read_excel("/Users/seopaul/Desktop/2018_2_BigData_Project/data/raw_data/전체데이터_서울_원본.xlsx")

    # 통합.xlsx 불러오기
    store = pd.read_excel("/Users/seopaul/Desktop/2018_2_BigData_Project/data/통합.xlsx")

    # 지번주소 필터링
    jibun = raw_data[['소재지전체주소', '영업상태명']]
    # jibun = jibun[jibun['영업상태명'] == '영업']
    # jibun.index = pd.RangeIndex(len(jibun))

    result = jibun_filter(jibun['소재지전체주소'])

    # 저장
    store['프렌차이즈_원본_지번_주소_명'] = jibun['소재지전체주소']
    store['프렌차이즈_지번_주소_명'] = result
    store.to_excel("/Users/seopaul/Desktop/2018_2_BigData_Project/data/통합.xlsx", index=False)

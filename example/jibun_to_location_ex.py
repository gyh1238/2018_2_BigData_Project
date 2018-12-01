# -*- coding: utf-8 -*-
from mapAPI.transform import jibun_to_location
import pandas as pd

if __name__ == '__main__':
    # 통합.xlsx 불러오기
    store = pd.read_excel("/Users/seopaul/Desktop/2018_2_BigData_Project/data/통합(Test).xlsx")

    # 지번주소 -> 위도,경도
    location = jibun_to_location(store['프렌차이즈_지번_주소_명'], atype='Naver')

    # 저장
    store['프렌차이즈_위도'] = location[0]
    store['프렌차이즈_경도'] = location[1]
    store.to_excel("/Users/seopaul/Desktop/2018_2_BigData_Project/data/통합(Test).xlsx", index=False)



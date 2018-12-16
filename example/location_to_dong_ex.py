from mapAPI.v1.transform import location_to_dong

import pandas as pd

if __name__ == '__main__':
    # 전체데이터.xlsx 데이터 전처리
    raw_data = pd.read_excel("/Users/seopaul/Desktop/2018_2_BigData_Project/전체데이터.xlsx")

    # 위도,경도 -> 동이름
    dong = location_to_dong(raw_data['프렌차이즈_위도'],raw_data['프렌차이즈_경도'], atype='NaverReverse')
    # 정리 및 저장
    result = dong
    result.to_excel("/Users/seopaul/Desktop/2018_2_BigData_Project/동뽑기.xlsx", index=False)

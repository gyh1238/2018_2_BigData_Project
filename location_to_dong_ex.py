from mapAPI.transform import location_to_dong

import pandas as pd

if __name__ == '__main__':
    # 스타벅스.xlsx 데이터 전처리
    raw_data = pd.read_excel("C:/Users/YeoChunghyun/Desktop/전체데이터.xlsx")

    # 위도,경도 -> 동이름
    dong = location_to_dong(raw_data['프렌차이즈_위도'],raw_data['프렌차이즈_경도'], atype='NaverReverse')
    # 정리 및 저장
    result=dong
    result.to_excel("C:/Users/YeoChunghyun/Desktop/동뽑기.xlsx", index=False)

from test import *
import pandas as pd


if __name__ == '__main__':
    # 스타벅스.xlsx 데이터 전처리
    raw_data = pd.read_excel("/Users/seopaul/Desktop/BD_Project/data/raw_data/스타벅스.xlsx")
    data = raw_data[['소재지전체주소', '사업장명', '영업상태명']]

    # 지번주소 필터링
    jibun = raw_data['소재지전체주소']
    jibun = jibun_filter(jibun)
    data = data.copy()
    data['지번주소'] = jibun

    # 지번주소 -> 위도,경도
    location = jibun_to_location(jibun)
    data = data.copy()
    data['위도'] = location[0]
    data['경도'] = location[1]

    # 정리 및 저장
    data = pd.DataFrame(data, columns=['소재지전체주소', '지번주소', '사업장명', '영업상태명', '위도', '경도'])
    save_excel(data, "/Users/seopaul/Desktop/BD_Project/data/스타벅스.xlsx")
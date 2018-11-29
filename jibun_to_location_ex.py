from mapAPI.filter import jibun_filter
from mapAPI.transform import jibun_to_location
import pandas as pd

if __name__ == '__main__':
    # 전체데이터_서울_원본.xlsx 불러오기
    raw_data = pd.read_excel("/Users/seopaul/Desktop/2018_2_BigData_Project/data/raw_data/전체데이터_서울_원본.xlsx")
    data = raw_data[['소재지전체주소', '사업장명', '영업상태명']]

    # 통합.xlsx 불러오기
    store = pd.read_excel("/Users/seopaul/Desktop/2018_2_BigData_Project/data/통합.xlsx")

    # 지번주소 필터링
    jibun = raw_data['소재지전체주소']
    jibun = jibun_filter(jibun)
    print(len(raw_data))
    print(len(jibun))
    
    # 저장
    store['프렌차이즈_지번_주소_명'] = jibun
    store.to_excel("/Users/seopaul/Desktop/2018_2_BigData_Project/data/통합.xlsx", index=False)

    '''
    # 지번주소 -> 위도,경도
    location = jibun_to_location(jibun, atype='Google')

    # 저장
    store['프렌차이즈_위도'] = location[0]
    store['프렌차이즈_경도'] = location[1]
    store.to_excel("/Users/seopaul/Desktop/2018_2_BigData_Project/data/통합.xlsx", index=False)
    '''


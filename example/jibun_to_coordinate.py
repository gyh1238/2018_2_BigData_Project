from mapAPI.v2.transform_v2 import JibunToCoordinate
import pandas as pd

if __name__ == '__main__':
    jibun_to_coordinate_google = JibunToCoordinate('Google')  # Google API
    jibun_to_coordinate_naver = JibunToCoordinate('Naver')  # Naver API

    # str type data
    data_a = '서울특별시 종로구 명륜1가 36-27'

    # list type data
    data_b = ['서울특별시 종로구 명륜1가 36-27', '서울특별시 종로구 명륜1가 36-23']

    # Series type data
    data_c = pd.Series(data_b)

    # Output type: dict
    result_google_a = jibun_to_coordinate_google(data_a)
    result_google_b = jibun_to_coordinate_google(data_b)
    result_google_c = jibun_to_coordinate_google(data_c)

    result_naver_a = jibun_to_coordinate_naver(data_a)
    result_naver_b = jibun_to_coordinate_naver(data_b)
    result_naver_c = jibun_to_coordinate_naver(data_c)

from mapAPI.transform import location_to_manhattan
import pandas as pd

if __name__ == '__main__':
    raw_data = pd.read_excel("/Users/seopaul/Desktop/2018_2_BigData_Project/data/스타벅스.xlsx")

    data = raw_data[['위도', '경도']]
    result = location_to_manhattan(data, data, distance=0.01)



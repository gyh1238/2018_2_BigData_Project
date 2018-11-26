from mapAPI.tools import Tools
import pandas as pd

if __name__ == '__main__':
    raw_data = pd.read_excel("/Users/seopaul/Desktop/2018_2_BigData_Project/data/스타벅스.xlsx")
    data = raw_data[['위도', '경도', '사업장명']]

    t = Tools()
    t.add_marker(data)
    t.save("/Users/seopaul/Desktop/2018_2_BigData_Project/data/map/map1.html")

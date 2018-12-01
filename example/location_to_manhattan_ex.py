from mapAPI.transform import location_to_manhattan
import pandas as pd

if __name__ == '__main__':
    raw_store = pd.read_excel("/Users/seopaul/Desktop/2018_2_BigData_Project/data/통합.xlsx")
    raw_bus = pd.read_excel("//Users/seopaul/Desktop/2018_2_BigData_Project/data/raw_data/2018버스정류장.xlsx")
    raw_crosswalk = pd.read_excel("//Users/seopaul/Desktop/2018_2_BigData_Project/data/raw_data/2018횡단보도.xlsx")

    store = raw_store[['프렌차이즈_위도', '프렌차이즈_경도']]
    bus = raw_bus[['위도', '경도']]
    crosswalk = raw_crosswalk[['위도', '경도']]

    # Count Bus Station distance < 0.002(200m)
    result = location_to_manhattan(store, bus, distance=0.002)
    raw_store['버스정류장_갯수'] = result['count']

    # Count Crosswalk distance < 0.001(100m)
    result = location_to_manhattan(store, crosswalk, distance=0.001)
    raw_store['횡단보도_갯수'] = result['count']

    # Save DataFrame to Excel(*.xlsx)
    raw_store.to_excel("/Users/seopaul/Desktop/2018_2_BigData_Project/data/통합.xlsx", index=False)



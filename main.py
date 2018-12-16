from mapAPI.v2.filter_v2 import JibunFilter
from mapAPI.v2.transform_v2 import JibunToCoordinate, CoordinateToManhattan
import folium

if __name__ == '__main__':
    jibun_filter = JibunFilter()
    jibun_to_coordinate = JibunToCoordinate(atype='Naver')
    coordinate_to_manhattan = CoordinateToManhattan()

    search_data = '서울특별시 종로구 명륜1가 36-27번지'
    filtered_data = jibun_filter(search_data)
    coordinate_data = jibun_to_coordinate(filtered_data)

    result = coordinate_to_manhattan(coordinate_data,
                                     distance={'BUS': 0.002, 'CROSSWALK': 0.001, 'SUBWAY': 0.01, 'POPULATION': 0.015})

    # Make a map using result data
    m = folium.Map([coordinate_data['lat'][0], coordinate_data['lng'][0]], zoom_start=15, tiles='OpenStreetMap')
    folium.Marker([coordinate_data['lat'][0], coordinate_data['lng'][0]]).add_to(m)
    for r in result:
        a = r['정류장']['정보']
        for t in a:
            folium.Marker([t[2], t[3]], popup=t[1], icon=folium.Icon(color='red')).add_to(m)

        b = r['횡단보도']['정보']
        for t in b:
            folium.Marker([t[2], t[3]], popup=t[1], icon=folium.Icon(color='green')).add_to(m)

        c = r['지하철']['정보']
        folium.Marker([c[1], c[2]], popup=c[0], icon=folium.Icon(color='blue')).add_to(m)

        d = r['유동인구']['정보']
        folium.CircleMarker([d[4], d[5]], radius=50, popup=d[1], color='#3186cc').add_to(m)
    m.save("/Users/seopaul/Desktop/2018_2_BigData_Project/data/map/test.html")






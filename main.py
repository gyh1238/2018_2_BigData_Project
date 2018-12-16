from mapAPI.v2.filter_v2 import JibunFilter
from mapAPI.v2.transform_v2 import JibunToCoordinate, CoordinateToManhattan
from folium.plugins import MarkerCluster
from folium.map import Icon, Popup
import folium

if __name__ == '__main__':
    jibun_filter = JibunFilter()  # Jibun Filtering Object
    naver_api = JibunToCoordinate(atype='Naver')  # Naver API
    google_api = JibunToCoordinate(atype='Google')  # Google API
    coordinate_to_manhattan = CoordinateToManhattan()  # Manhattan distance Calculator Object

    search_data = '서울특별시 종로구 창신동 372-0번지'
    filtered_data = jibun_filter(search_data)

    coordinate_data = naver_api(filtered_data)

    result = coordinate_to_manhattan(coordinate_data,
                                     distance={'BUS': 0.002, 'CROSSWALK': 0.001, 'SUBWAY': 0.015, 'POPULATION': 0.015})

    # Make a map using result data
    icon = {'station': Icon(color='red', icon='coffee', prefix='fa'),
            'crosswalk': Icon(color='purple'),
            'subway': Icon(color='orange'),
            }

    m = folium.Map([coordinate_data['lat'][0], coordinate_data['lng'][0]],
                   max_zoom=20, min_zoom=12, zoom_start=15, tiles='OpenStreetMap')

    folium.Marker([coordinate_data['lat'][0], coordinate_data['lng'][0]]).add_to(m)
    station_marker = MarkerCluster().add_to(m)
    crosswalk_marker = MarkerCluster().add_to(m)

    for r in result:
        a = r['정류장']['정보']
        try:
            for t in a:
                folium.Marker([t[2], t[3]], popup='<정류장> ' + t[1], icon=folium.Icon(color='red')).add_to(station_marker)
        except ValueError:
            pass

        b = r['횡단보도']['정보']
        try:
            for t in b:
                folium.Marker([t[2], t[3]], popup='<횡단보도> ' + t[1], icon=folium.Icon(color='purple')).add_to(crosswalk_marker)
        except ValueError:
            pass

        c = r['지하철']['정보']
        try:
            folium.Marker([c[1], c[2]], popup='<지하철> ' + c[0], icon=folium.Icon(color='blue')).add_to(m)
        except TypeError:
            pass

        d = r['유동인구']['정보']
        try:
            folium.Circle(location=[d[4], d[5]], popup='<상권> ' + d[1], radius=300).add_to(m)
        except ValueError:
            pass

    m.save("/Users/seopaul/Desktop/2018_2_BigData_Project/data/map/test.html")






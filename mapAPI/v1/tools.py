# -*- coding: utf-8 -*-
from folium import plugins
import folium


class Tools:
    def __init__(self):
        self.init_pose = [37.5653161, 126.9745883]
        self.init_zoom = 12
        self.map = folium.Map(self.init_pose, zoom_start=self.init_zoom, tiles='OpenStreetMap')

    # Marker를 추가하는 함수
    def add_marker(self, data):
        marker_list = list()
        popup_flag = None
        if '위도' not in data or '경도' not in data:
            raise ValueError
        if len(data) > 2:
            popup_flag = True

        if popup_flag is False:
            for i in range(data.shape[0]):
                try:
                    marker_list.append(folium.Marker([data['위도'][i], data['경도'][i]]))
                except ValueError:
                    pass
        else:
            for i in range(data.shape[0]):
                try:
                    marker_list.append(folium.Marker([data['위도'][i], data['경도'][i]], popup=data['사업장명'][i]))
                except ValueError:
                    pass
        return marker_list

    def remove_marker(self, data):
        print("test")

    def search(self, data):
        plugins.Search(data, search_zoom=15).add_to(self.map)

    def save(self, path):
        self.map.save(path)

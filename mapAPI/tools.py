import folium


class Tools:
    def __init__(self):
        self.init_pose = [37.5653161, 126.9745883]
        self.init_zoom = 12
        self.map = folium.Map(self.init_pose, zoom_start=self.init_zoom, tiles='Stamen Terrain')

    # Marker를 추가하는 함수
    def add_marker(self, data):
        for i in range(0, len(data)):
            try:
                folium.Marker([data.iloc[i]['위도'], data.iloc[i]['경도']], popup=data.iloc[i]['사업장명']).add_to(self.map)
            except ValueError:
                pass

    def remove_marker(self, data):
        print("test")

    def save(self, path):
        self.map.save(path)

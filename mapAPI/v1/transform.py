# -*- coding: utf-8 -*-
from pandas import Series, DataFrame
import numpy as np
from urllib.parse import quote
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json
import pandas as pd


def jibun_to_location(data, atype='Google'):
    location_list = list()
    latitude_list = list()
    longitude_list = list()

    # Google API
    if atype == 'Google':
        url = 'https://maps.googleapis.com/maps/api/geocode/json?language=ko&address='
        key = '&key=AIzaSyCztxwqctO8tl6CDL4sfva0HhEuvbUyxtw'

        count = 0
        for d in data:
            address = quote(d)
            addr = json.loads(urlopen(url + address + key).read().decode('utf-8'))
            if addr['status'] == 'OK':
                if len(addr['results']) == 1:
                    latitude_list.append(addr['results'][0]['geometry']['location']['lat'])
                    longitude_list.append(addr['results'][0]['geometry']['location']['lng'])
                else:
                    lat = np.nan
                    lng = np.nan
                    for rst in addr['results']:
                        if rst['formatted_address'] == d:
                            lat = rst['geometry']['location']['lat']
                            lng = rst['geometry']['location']['lng']
                            break
                    latitude_list.append(lat)
                    longitude_list.append(lng)
            else:
                latitude_list.append(np.nan)
                longitude_list.append(np.nan)
            count += 1
            if count % 100 == 0:
                print(str(count))

    # Naver API
    elif atype == 'Naver':
        url = 'https://openapi.naver.com/v1/map/geocode?query='
        client_id = 'YgvwOV94B4syvCpdeTIU'
        client_secret = 'xYNaoADxvs'

        count = 0
        for d in data:
            address = quote(d)
            request = Request(url + address)
            request.add_header("X-Naver-Client-Id", client_id)
            request.add_header("X-Naver-Client-Secret", client_secret)

            try:
                response = urlopen(request)
            except HTTPError:
                latitude_list.append(np.nan)
                longitude_list.append(np.nan)
            else:
                if response.getcode() == 200:
                    addr = json.loads(response.read().decode('utf-8'))
                    if addr['result']['total'] == 1:
                        latitude_list.append(addr['result']['items'][0]['point']['y'])
                        longitude_list.append(addr['result']['items'][0]['point']['x'])
                    elif addr['result']['total'] > 1:
                        lat = np.nan
                        lng = np.nan
                        for rst in addr['result']['items']:
                            if rst['address'] == d:
                                lat = rst['point']['y']
                                lng = rst['point']['x']
                                break
                        latitude_list.append(lat)
                        longitude_list.append(lng)
                    else:
                        raise ValueError
                else:
                    raise ValueError
            count += 1
            if count % 100 == 0:
                print(str(count))
    else:
        raise KeyError

    location_list.append(Series(latitude_list, name='위도'))
    location_list.append(Series(longitude_list, name='경도'))
    return location_list


def location_to_manhattan(data, feature, distance=0.01):
    """
    1. |스타벅스의 위도 - 좌표의 위도| + |스타벅스의 경도 - 좌표의 경도| = Manhattan Distance
    2. dict("lat": " ", "lng": " ", "count":" ") append to list
    """
    results = list()
    for i in range(0, len(data)):
        tmp = feature[abs(feature['위도'] - data.iloc[i]['프렌차이즈_위도'])
                      + abs(feature['경도'] - data.iloc[i]['프렌차이즈_경도']) < distance]
        results.append(
            dict({"center": [data.iloc[i]['프렌차이즈_위도'], data.iloc[i]['프렌차이즈_경도']],
                  "feature": tmp.values,
                  "count": tmp.shape[0]}
                 )
        )

    return DataFrame(results)


def location_to_test(data, feature, distance=0.005):
    results = list()
    for i in range(0, len(data)):
        tmp = feature[abs(feature['위도'] - data.iloc[i]['프렌차이즈_위도'])
                      + abs(feature['경도'] - data.iloc[i]['프렌차이즈_경도']) < distance]

        dt = [abs(d[0] - data.iloc[i]['프렌차이즈_위도']) + abs(d[1] - data.iloc[i]['프렌차이즈_경도']) for d in tmp.values]
        try:
            idx = dt.index(min(dt))
        except ValueError:
            results.append({"lat": np.nan, "lng": np.nan})
        else:
            results.append({"lat": tmp.values[idx][0], "lng": tmp.values[idx][1]})

    return DataFrame(results)


def location_to_dong(datax, datay, atype='NaverReverse'):
    dong_list = pd.DataFrame(columns=['행정동'])
    # Naver API
    if atype == 'NaverReverse':
        url = 'https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc?request=coordsToaddr&version=1.0&coords='
        client_id = 'mjw9rfcjez'
        client_secret = 'hbwLGzQe7XOLx5rKZS9iak3CZlDFJ8G5KR1TZ0xL'
        temp=datax.to_frame().join(datay)
        temp['위경도'] = temp.apply(lambda x: '%s,%s' % (x['프렌차이즈_경도'], x['프렌차이즈_위도']), axis=1)
        data= temp['위경도']
        for d in data:
            address = quote(d)
            request = Request(url + address+'&sourcecrs=epsg:4326&output=json&orders=admcode')
            request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
            request.add_header("X-NCP-APIGW-API-KEY", client_secret)
            dong=np.nan
            try:
                response = urlopen(request)
            except HTTPError:
                dong_list.add(np.nan)
            else:
                if response.getcode() == 200:
                    addr = json.loads(response.read().decode('utf-8'))
                    dong = addr['results'][0]['region']['area3']['name']
                    dong_list = dong_list.append({'행정동': dong}, ignore_index=True)
                    print(dong)
                else:
                    raise ValueError
    else:
        raise KeyError

    return dong_list



# -*- coding: utf-8 -*-
from pandas import Series, DataFrame
import numpy as np
from urllib.parse import quote
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json


def jibun_to_location(data, atype='Google'):
    location_list = list()
    latitude_list = list()
    longitude_list = list()

    # Google API
    if atype == 'Google':
        url = 'https://maps.googleapis.com/maps/api/geocode/json?language=ko&address='
        key = '&key=AIzaSyCztxwqctO8tl6CDL4sfva0HhEuvbUyxtw'

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

    # Naver API
    elif atype == 'Naver':
        url = 'https://openapi.naver.com/v1/map/geocode?query='
        client_id = 'YgvwOV94B4syvCpdeTIU'
        client_secret = 'xYNaoADxvs'

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

    location_list.append(Series(latitude_list, name='위도'))
    location_list.append(Series(longitude_list, name='경도'))
    return location_list


def location_to_manhattan():
    print("Test")

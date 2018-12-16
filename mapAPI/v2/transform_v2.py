# -*- coding: utf-8 -*-
from pandas import Series, DataFrame
from numpy import ndarray
from urllib.parse import quote, unquote
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import pandas as pd
import numpy as np
import json


class JibunToCoordinate:
    """
    This class transforms from jibun address to latitude, longitude coordinates.
    """
    def __init__(self, atype):
        self.__atype = atype
        self.__info = dict()
        self.__set_format(atype)

    def set_client_info(self, client_id, client_secret):
        if self.__info['TYPE'] == 'naver':
            self.__info['CLIENT_ID'] = client_id
            self.__info['CLIENT_SECRET'] = client_secret
        else:
            raise ValueError

    def set_key(self, key):
        if self.__info['TYPE'] == 'google':
            self.__info['KEY'] = key
        else:
            raise ValueError

    def __set_format(self, atype):
        if not isinstance(atype, str):
            raise TypeError

        if atype.lower() == 'google':
            self.__info = {'TYPE': 'google',
                           'URL': 'https://maps.googleapis.com/maps/api/geocode/json',
                           'QUERY': {'language': 'ko', 'address': None, 'key': 'AIzaSyCztxwqctO8tl6CDL4sfva0HhEuvbUyxtw'}
                           }
        elif atype.lower() == 'naver':
            self.__info = {'TYPE': 'naver',
                           'URL': 'https://openapi.naver.com/v1/map/geocode',
                           'QUERY': {'address': None},
                           'CLIENT_ID': 'YgvwOV94B4syvCpdeTIU',
                           'CLIENT_SECRET': 'xYNaoADxvs'
                           }
        else:
            raise ValueError

    def __set_query(self):
        if self.__info['TYPE'] == 'google':
            query = "?" + "&".join(["=".join(t) for t in self.__info['QUERY'].items()])
        else:
            query = "?query=" + self.__info['QUERY']['address']
        return query

    def __call__(self, data):
        # Data Type Check
        if not isinstance(data, (ndarray, Series, list, str)):
            raise TypeError

        # Data handling str type
        if isinstance(data, str):
            data = [data]

        # From data to quoted data
        address = [quote(d) for d in data]

        # Make Query & Call API
        result = {'lat': list(), 'lng': list()}
        for addr in address:
            self.__info['QUERY']['address'] = addr
            query = self.__set_query()

            request = Request(self.__info['URL'] + query)
            if self.__info['TYPE'] == 'naver':
                request.add_header("X-Naver-Client-Id", self.__info['CLIENT_ID'])
                request.add_header("X-Naver-Client-Secret", self.__info['CLIENT_SECRET'])

            try:
                response = urlopen(request)
            except HTTPError:
                result['lat'].append(np.nan)
                result['lng'].append(np.nan)
            else:
                if response.getcode() == 200:
                    info = json.loads(response.read().decode('utf-8'))
                else:
                    raise HTTPError

                if self.__info['TYPE'] == 'google':
                    if info['status'] == 'OK':
                        if len(info['results']) == 1:
                            result['lat'].append(info['results'][0]['geometry']['location']['lat'])
                            result['lng'].append(info['results'][0]['geometry']['location']['lng'])
                        else:
                            lat = np.nan
                            lng = np.nan
                            for rst in info['results']:
                                if rst['formatted_address'] == unquote(addr):
                                    lat = rst['geometry']['location']['lat']
                                    lng = rst['geometry']['location']['lng']
                                    break
                            result['lat'].append(lat)
                            result['lng'].append(lng)
                    else:
                        result['lat'].append(np.nan)
                        result['lng'].append(np.nan)
                else:
                    if info['result']['total'] == 1:
                        result['lat'].append(info['result']['items'][0]['point']['y'])
                        result['lng'].append(info['result']['items'][0]['point']['x'])
                    else:
                        lat = np.nan
                        lng = np.nan
                        for rst in info['result']['items']:
                            if rst['address'] == unquote(addr):
                                lat = rst['point']['y']
                                lng = rst['point']['x']
                                break
                        result['lat'].append(lat)
                        result['lng'].append(lng)
        return result


class CoordinateToManhattan:
    """
        This class transforms from latitude, longitude coordinates to manhattan distance info.
    """
    def __init__(self):
        self.__bus = pd.read_excel("/Users/seopaul/Desktop/2018_2_BigData_Project/data/2018버스정류장.xlsx")
        self.__crosswalk = pd.read_excel("/Users/seopaul/Desktop/2018_2_BigData_Project/data/2018횡단보도.xlsx")
        self.__subway = pd.read_excel("/Users/seopaul/Desktop/2018_2_BigData_Project/data/2018지하철.xlsx")
        self.__population = pd.read_excel("/Users/seopaul/Desktop/2018_2_BigData_Project/data/2018유동인구.xlsx")

        self.distance = {'BUS': None, 'CROSSWALK': None, 'SUBWAY': None, 'POPULATION': None}

    def calc_manhattan(self, data, flag):
        if flag == 'BUS':
            feature = self.__bus
        elif flag == 'CROSSWALK':
            feature = self.__crosswalk
        elif flag == 'SUBWAY':
            feature = self.__subway
        elif flag == 'POPULATION':
            feature = self.__population
        else:
            raise ValueError('Wrong Flag')
        return feature[abs(feature['위도'] - data[0]) + abs(feature['경도'] - data[1]) < self.distance[flag]]

    def __call__(self, data, distance):
        """
            버스정류장 -> data: 매장 위경도, feature: 버스정류장 위경도, distance: 최대거리
                    output: 정류장명, 위도, 경도, 정류장갯수
            횡단보도 -> data: 매장 위경도, feature: 횡단보도 위경도, distance: 최대거리
                    output: 횡단보도코드, 위도, 경도, 횡단보도갯수
            지하철역 -> data: 매장 위경도, feature: 지하철역 위경도, distance: 최대거리
                    output: 지하철역명, 위도, 경도, 거리
            유동인구 -> data: 매장 위경도, feature: 상권 위경도, distance: 최대거리
                    output: 상권명, 위도, 경도, 유동인구
        """
        # Data Type Check
        if not isinstance(data, (list, dict)):
            raise TypeError('Wrong data type. (Required list, dict type)')

        # From raw data to ndarray type data
        if isinstance(data, list):
            data = np.array(data)
        else:
            data = np.array([value for value in data.values()]).T

        # ndarray Dimension Check
        if len(data.shape) != 2:
            raise ValueError('Dimension mismatch. (Required 2 dimension, Now ' + str(len(data.shape)) + ' dimension)')

        # Distance Type Check
        if not isinstance(distance, dict):
            raise TypeError("Dictionary data type is required.")
        if 'BUS' and 'CROSSWALK' and 'SUBWAY' and 'POPULATION' not in distance.keys():
            raise TypeError("Data Format {'BUS': Value, 'CROSSWALK': Value', "
                            "'SUBWAY: Value, 'POPULATION: Value} is required.")
        else:
            self.distance = distance

        result = list()
        for d in data:
            info = {'정류장': {'정보': None, '갯수': None},
                    '횡단보도': {'정보': None, '갯수': None},
                    '지하철': {'정보': None, '거리': None},
                    '유동인구': {'정보': None, '인구수': None}}
            if distance['BUS'] is not None:
                tmp = self.calc_manhattan(d, 'BUS')
                info['정류장']['정보'] = tmp.values
                info['정류장']['갯수'] = tmp.shape[0]

            if distance['CROSSWALK'] is not None:
                tmp = self.calc_manhattan(d, 'CROSSWALK')
                info['횡단보도']['정보'] = tmp.values
                info['횡단보도']['갯수'] = tmp.shape[0]

            if distance['SUBWAY'] is not None:
                tmp = self.calc_manhattan(d, 'SUBWAY')

                dt = [abs(t[1] - d[0]) + abs(t[2] - d[1]) for t in tmp.values]
                try:
                    idx = dt.index(min(dt))
                    dt = min(dt)
                except ValueError:
                    pass
                else:
                    info['지하철']['정보'] = tmp.values[idx]
                    info['지하철']['거리'] = dt

            if distance['POPULATION'] is not None:
                tmp = self.calc_manhattan(d, 'POPULATION')

                dt = [abs(t[4] - d[0]) + abs(t[5] - d[1]) for t in tmp.values]
                try:
                    idx = dt.index(min(dt))
                except ValueError:
                    pass
                else:
                    info['유동인구']['정보'] = tmp.values[idx]
                    info['유동인구']['인구수'] = tmp.values[idx][2]
            result.append(info)
        return result


if __name__ == '__main__':
    pass


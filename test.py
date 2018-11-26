# -*- coding: utf-8 -*-
from pandas import Series, DataFrame
import numpy as np

from urllib.parse import quote, quote_plus, urlencode
from urllib.request import urlopen, Request
import xml.etree.ElementTree as ET
import json
import time


def jibun_filter(data):
    jibun_list = list()
    element = {'do': "", 'si': "", 'gu': "", 'dong': "", 'bunji': ""}
    for d in data:
        tmp = d.split(" ")

        if tmp[0][-1:] == '도':
            element['do'] = tmp[0]
            for t in tmp[1:]:
                if t[-1:] == '시' or t[-1:] == '군':
                    element['si'] = t
                elif t[-1:] == '구' or t[-1:] == '면' or t[-1:] == '읍':
                    element['gu'] = t
                elif t[-1:] == '동' or t[-1:] == '리':
                    element['dong'] = t
                elif t[-2:] == '번지':
                    element['bunji'] = t[:-2]
                    jibun = element['do'] + " " + element['si'] + " " + element['gu'] + " " + element["dong"] + " " + element["bunji"]
                    jibun_list.append(jibun)
                else:
                    pass
        elif tmp[0][-1:] == '시':
            element['si'] = tmp[0]
            for t in tmp[1:]:
                if t[-1:] == '구':
                    element['gu'] = t
                elif t[-1:] == '동' or t[-1:] == '가':
                    element['dong'] = t
                elif t[-2:] == '번지':
                    element['bunji'] = t[:-2]
                    jibun = element['si'] + " " + element['gu'] + " " + element["dong"] + " " + element["bunji"]
                    jibun_list.append(jibun)
                else:
                    pass
        else:
            pass
    return Series(jibun_list, name='지번주소')


def jibun_to_location(data):
    location_list = list()
    latitude_list = list()
    longitude_list = list()

    url = 'https://maps.googleapis.com/maps/api/geocode/json?language=ko&address='
    key = '&key=AIzaSyCztxwqctO8tl6CDL4sfva0HhEuvbUyxtw'

    for d in data:
        t1 = time.time()
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
        t2 = time.time()
        print(t2 - t1)
    location_list.append(Series(latitude_list, name='위도'))
    location_list.append(Series(longitude_list, name='경도'))
    return location_list


def save_excel(data, path):
    try:
        data.to_excel(path, index=False)
        return True
    except Exception as e:
        print("[ERROR]Save Failed -> " + str(e))
        return False

"""
def jibun_to_doro(data, rtype='json'):
    if rtype == 'json':
        result_type = rtype
    elif rtype == 'xml':
        result_type = rtype
    else:
        raise ValueError

    address_list = list()
    url = 'http://www.juso.go.kr/addrlink/addrLinkApi.do'
    for d in data:
        query_params = '?' + urlencode(
            {quote_plus('currentPage'): '1', quote_plus('countPerPage'): '20', quote_plus('resultType'): result_type,
             quote_plus('keyword'): d, quote_plus('confmKey'): 'U01TX0FVVEgyMDE4MTEyMzE4MDYyNDEwODMxOTc='})

        request = Request(url + query_params)
        request.get_method = lambda: 'GET'
        response_body = urlopen(request).read()

        if result_type == 'json':
            response = json.loads(response_body)
            result = response['results']['juso']

            address = None
            if len(result) == 1:
                address = result[0]['roadAddr']
            elif len(result) == 0:
                address = np.nan
            else:
                for i in range(len(result)):
                    if result[i]['jibunAddr'] == d:
                        address = result[i]['roadAddr']
                        break
                if address is None:
                    address = np.nan
            address_list.append(address)
        else:
            print("XML")
    return Series(address_list, name='도로명주소')
"""

if __name__ == '__main__':
    pass


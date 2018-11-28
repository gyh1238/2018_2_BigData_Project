# -*- coding: utf-8 -*-
from pandas import Series, DataFrame
import numpy as np


def jibun_filter(data):
    jibun_list = list()
    element = {'do': "", 'si': "", 'gu': "", 'dong': "", 'bunji': ""}
    for d in data:
        try:
            tmp = d.split(" ")
        except AttributeError:
            jibun_list.append(np.nan)
        else:
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
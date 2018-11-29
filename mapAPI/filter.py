# -*- coding: utf-8 -*-
from pandas import Series, DataFrame


def jibun_filter(data):
    jibun_list = list()
    for d in data:
        try:
            tmp = d.split(" ")
        except AttributeError:
            jibun_list.append("입력주소없음")
            continue

        idx = None
        element = {'do': "", 'si': "", 'gu': "", 'dong': "", 'bunji': ""}
        for i, t in enumerate(tmp):
            if t[-2:] == '번지':
                idx = i + 1
                break

        if tmp[0][-1:] == '도':
            tmp = tmp[0:idx]
            element['do'] = tmp[0]
            for t in tmp[1:]:
                if t[-1:] == '시':
                    element['si'] = t
                elif t[-1:] == '구':
                    element['gu'] = t
                elif t[-1:] == '동' or t[-1:] == '가' or t[-1:] == '로':
                    element['dong'] = t
                elif t[-2:] == '번지':
                    element['bunji'] = t[:-2]
                else:
                    continue
            if element['do'] != "" and element['si'] != "" and element['gu'] != "" and element['dong'] != "" and element['bunji'] != "":
                jibun_list.append(" ".join(list(element.values())))
            else:
                jibun_list.append('입력주소오류')
        elif tmp[0][-1:] == '시':
            tmp = tmp[0:idx]
            element['si'] = tmp[0]
            for t in tmp[1:]:
                if t[-1:] == '구':
                    element['gu'] = t
                elif t[-1:] == '동' or t[-1:] == '가' or t[-1:] == '로':
                    element['dong'] = t
                elif t[-2:] == '번지':
                    element['bunji'] = t[:-2]
                else:
                    continue
            if element['si'] != "" and element['gu'] != "" and element['dong'] != "" and element['bunji'] != "":
                jibun = " ".join(list(element.values())[1:])
                jibun_list.append(jibun)
            else:
                jibun_list.append('입력주소오류')
        else:
            jibun_list.append("입력주소오류")
    return Series(jibun_list, name='지번주소')

# -*- coding: utf-8 -*-


def save_excel(data, path):
    try:
        data.to_excel(path, index=False)
        return True
    except Exception as e:
        print("[ERROR]Save Failed -> " + str(e))
        return False

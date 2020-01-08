#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import os
import pickle

from src.globals.globals import GlobalContainer


local_path = os.path.join(os.getcwd(), "src/globals/local")


def get_local_info():
    """
    获取本地信息
    """
    if os.path.exists(local_path):
        with open(local_path, "rb") as f:
            json_bytes = f.read()
            json_info = pickle.loads(json_bytes)
    else:
        json_info = {}
        with open(local_path, "wb") as f:
            f.write(pickle.dumps(json_info))
    return json_info


def set_local_info(key, value):
    """
    保存本地信息
    :return:
    """
    with open(local_path, "rb+") as f:
        json_bytes = f.read()
        json_info = pickle.loads(json_bytes)
        json_info[key] = value
        f.seek(0)
        f.write(pickle.dumps(json_info))


global_config = GlobalContainer()
global_config.hostname = 'http://joucks.cn:3344'
global_config.ws_server = ['http://joucks.cn:3356', 'http://joucks.cn:3358']


global_config.local = get_local_info()

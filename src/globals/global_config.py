#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import json
import os

from src.globals.globals import GlobalContainer


local_path = os.path.join(os.getcwd(), "src/globals/local.json")


def get_local_info():
    """
    获取本地信息
    """
    if os.path.exists(local_path):
        with open(local_path, "r+") as f:
            json_info = json.load(f)
    else:
        json_info = {}
        with open(local_path, "w") as w:
            json.dump(json_info, w)
    return json_info


def set_local_info(key, value):
    """
    保存本地信息
    :return:
    """
    with open(local_path, "r+") as f:
        json_info = json.load(f)
        json_info[key] = value
        f.seek(0)
        json.dump(json_info, f)


global_config = GlobalContainer()
global_config.hostname = 'http://joucks.cn:3344'
global_config.ws_server = ['http://joucks.cn:3356', 'http://joucks.cn:3358']


local_info = get_local_info()
global_config.username = local_info.get("username", "")

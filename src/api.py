#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
from src.global_config import global_config
from src.globals import GlobalContainer


def gen_api(uri: str) -> str:
    return '{}{}'.format(global_config.hostname, uri)


api = GlobalContainer()

api.login = gen_api('/api/login')
api.user_init_info = gen_api('/api/getUserInitInfo')

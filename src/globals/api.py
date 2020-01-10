#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
from src.globals.global_config import global_config
from src.globals.globals import GlobalContainer


def gen_api(uri: str) -> str:
    return '{}{}'.format(global_config.hostname, uri)


api = GlobalContainer()

api.login = gen_api('/api/login')
api.logout = gen_api('/api/loginOut')
api.user_init_info = gen_api('/api/getUserInitInfo')
api.scene_list = gen_api('/api/getCombatBeMonster')

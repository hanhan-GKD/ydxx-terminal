#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
from src.globals.globals import GlobalContainer

global_values = GlobalContainer()

global_values.palette = [
    ('error_info', 'light red', ''),
    ('status_bar', 'white', 'light blue'),
    ('active_button', 'white', 'light red'),
    ('active_menu_item', 'white', 'light red'),
    ('active_channel_item', '', 'dark red'),
    ('team_mate_soldier', 'black', 'light green'),
    ('enemy_soldier', 'black', 'light red'),
    ('fight_info', 'light green', ''),
    ('info_remain_ph', 'dark red', ''),
    ('fight_user', 'dark red', ''),
    ('reward_goods', 'dark blue', ''),
    ('select_focus', 'light red', ''),
]
global_values.race_types = {
    1: '人',
    2: '魔',
    3: '妖',
    4: '精',
    '宠': '宠',
    '怪': '怪'
}
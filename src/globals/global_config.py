#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
from src.globals.globals import GlobalContainer

global_config = GlobalContainer()
global_config.hostname = 'http://joucks.cn:3344'
global_config.websocket_server = ['ws://joucks.cn:3356/socket.io', 'ws://joucks.cn:3358/socket.io']

#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
登录面板
"""
import asyncio

import aiohttp
import urwid

from src.globals.api import api
from src.globals.global_config import global_config
from src.globals.global_config import set_local_info
from src.globals.global_values import global_values
from src.ydxx_panel.main_panel import MainPanel
from src.ydxx_widget import button


class LoginPanel(urwid.WidgetPlaceholder):
    """
    登录面板
    """

    def __init__(self):

        def on_login(button):
            username = self.username_edit.get_edit_text()
            set_local_info("username", username)
            pwd = self.pwd_edit.get_edit_text()
            asyncio.get_event_loop().create_task(self.login(username, pwd))

        super(LoginPanel, self).__init__(urwid.SolidFill(' '))
        # 设置登录页面的logo
        logo = urwid.Text('')
#        with open('./logo.txt') as logo_file:
#            logo.set_text(logo_file.read())
        self.username_edit = urwid.Edit('账号: ')
        if global_config.username:
            self.username_edit.set_edit_text(global_config.username)
        self.pwd_edit = urwid.Edit('密码: ', mask='*')
        login_btn = button.Button('[登陆]', on_press=on_login)
        login_btn_wp = urwid.Padding(login_btn, align=urwid.CENTER, width='pack')
        self.login_result_info = urwid.Text('', align=urwid.CENTER)
        form = urwid.LineBox(
            urwid.Pile(
                [
                    self.username_edit, self.pwd_edit,
                    self.login_result_info, login_btn_wp
                ],
                focus_item=0
            )
        )
        self.original_widget = urwid.Overlay(
            urwid.ListBox(urwid.SimpleFocusListWalker([logo, form])),
            self.original_widget,
            align='center', width=45,
            valign='middle', height=('relative', 100),
            min_width=24, min_height=8,
            left=10, right=10)

    async def login(self, username, pwd):
        """
        登录
        """
        session = aiohttp.ClientSession()
        async with session.post(
                api.login, data={'user_name': username, 'user_pwd': pwd}
        ) as response:
            json_rst = await response.json()
            if 'code' in json_rst and json_rst['code'] == 200:
                user_data = json_rst['data']
                global_values.token = user_data['token']
                global_values.uid = user_data['_id']
                global_values.session = session
                self.original_widget = MainPanel()
            else:
                self.login_result_info.set_text(('error_info', '登录失败'))

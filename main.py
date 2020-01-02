#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import json

import urwid

from tornado import httpclient
from tornado.ioloop import IOLoop

from src import button
from src import menu_widget
from src.api import api
from src.global_values import global_values


class UserInfoPanel(urwid.LineBox):
    show_attr = [('nickname', '昵称: '),
                 ('level_text', '境界: '),
                 ('repair_num', '修为: '),
                 ('race_type', '种族: '),
                 ('ph_num', '气血值: '),
                 ('vitality_num', '活力: '),
                 ('force_num', '武力值: '),
                 ('physical_damage', '物理伤害: '),
                 ('iq_num', '智力值: '),
                 ('magic_damage', '魔法伤害: '),
                 ('endurance_num', '耐力值: '),
                 ('endurance_num', '耐力值: '),
                 ('physical_defense', '物理防御: '),
                 ('agile_num', '敏捷值: '),
                 ('magic_defense', '魔法防御: '),
                 ('faith_num', '信仰值: '),
                 ('restore_damage', '治疗伤害: '),
                 ('speed', '速度: '),
                 ('pet_max_count', '宠物上限: '),
                 ('health_num', '精力: '),
                 ('potential_num', '潜力点: ')]

    def __init__(self):
        self.attr_list = urwid.ListBox(urwid.SimpleFocusListWalker([]))
        super(UserInfoPanel, self).__init__(
            urwid.BoxAdapter(self.attr_list, 20), '用户信息')
        self.fetch_user_info()

    def fetch_user_info(self):
        def resp_user_info(response: httpclient.HTTPResponse):
            if response.code == 200:
                json_data = json.loads(response.body)
                if json_data['code'] == 200:
                    ready_extend_list = []
                    user = json_data['data']['user']
                    index = 0
                    show_attr = UserInfoPanel.show_attr
                    while index < len(show_attr):
                        if index + 1 < len(show_attr):
                            first_attr = show_attr[index]
                            second_attr = show_attr[index + 1]
                            ready_extend_list.append(
                                urwid.Columns([urwid.Text([first_attr[1], str(user[first_attr[0]])]),
                                               urwid.Text([second_attr[1], str(user[second_attr[0]])])]))
                        else:
                            attr = show_attr[index]
                            ready_extend_list.append(
                                urwid.Text([attr[1], str(user[attr[0]])]))
                        index += 2
                    self.attr_list.body.extend(ready_extend_list)

            else:
                pass

        request = httpclient.HTTPRequest(api.user_init_info, 'GET', headers={
            'Cookie': global_values.token})
        httpclient.AsyncHTTPClient().fetch(request, resp_user_info)


class MainPanel(urwid.Frame):

    def __init__(self):
        body = menu_widget.MenuWidget([('角色信息', UserInfoPanel()), ('背包', urwid.Text('背包: 空'))])

        footer = urwid.Text('--状态栏--')
        super(MainPanel, self).__init__(urwid.ListBox(urwid.SimpleFocusListWalker(
            [body])), footer=urwid.AttrMap(footer, 'status_bar'))


class LoginPanel(urwid.WidgetPlaceholder):

    def __init__(self):

        def on_login_result(response: httpclient.HTTPResponse):
            if response.code == 200:
                json_rst = json.loads(response.body)
                if 'code' in json_rst and json_rst['code'] == 200:
                    global_values.token = response.headers['Set-Cookie'].split(';')[
                        0]
                    self.original_widget = MainPanel()
                else:
                    self.login_result_info.set_text(('error_info', '登录失败'))

        def login(button):
            uname = self.uname_edit.get_edit_text()
            pwd = self.pwd_edit.get_edit_text()
            request = httpclient.HTTPRequest(
                api.login, 'POST', body='user_name={}&user_pwd={}'.format(uname, pwd))
            httpclient.AsyncHTTPClient().fetch(request, on_login_result)

        super(LoginPanel, self).__init__(urwid.SolidFill(' '))
        logo = urwid.Text('')
        with open('./logo.txt') as logo_file:
            logo.set_text(logo_file.read())
        self.uname_edit = urwid.Edit('账号: ')
        self.pwd_edit = urwid.Edit('密码: ', mask='*')
        login_btn = button.Button('[登陆]', on_press=login)
        login_btn_wp = urwid.Padding(
            login_btn, align=urwid.CENTER, width='pack')
        self.login_result_info = urwid.Text('', align=urwid.CENTER)
        form = urwid.LineBox(urwid.Pile(
            [self.uname_edit, self.pwd_edit, self.login_result_info, login_btn_wp], focus_item=0))
        self.original_widget = urwid.Overlay(
            urwid.ListBox(urwid.SimpleFocusListWalker([logo, form])),
            self.original_widget,
            align='center', width=45,
            valign='top', height=('relative', 100),
            min_width=24, min_height=8,
            left=10, right=10)


if __name__ == '__main__':
    main_panel = LoginPanel()
    loop = urwid.TornadoEventLoop(IOLoop())
    urwid.MainLoop(main_panel, palette=global_values.palette,
                   event_loop=loop).run()

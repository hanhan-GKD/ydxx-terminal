import urwid
from tornado import httpclient
from src.globals.global_values import global_values
from src.ydxx_panel.main_panel import MainPanel
import json
from src.globals.api import api
from src.ydxx_widget import button

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


import urwid
import tornado
from tornado.ioloop import IOLoop
from tornado import httpclient
from api import api
from global_values import global_values
import json


class UserInfoPanel(urwid.LineBox):
    show_attr = [('nickname', '昵称: '),
                 ('level_text', '境界: '),
                 ('repair_num', '修为: '),
                 ('race_type', '种族: '),
                 ('ph_num', '气血值: '),
                 ('vitality_num', '活力: ')]

    def __init__(self):
        self.attr_list = urwid.ListBox(urwid.SimpleFocusListWalker([]))
        super(UserInfoPanel, self).__init__(urwid.BoxAdapter(self.attr_list, 20), '用户信息')
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
                            ready_extend_list.append(urwid.Columns([urwid.Text([first_attr[1], str(user[first_attr[0]])]),
                                                                    urwid.Text([second_attr[1], str(user[second_attr[0]])])]))
                        else:
                            attr = show_attr[index]
                            ready_extend_list.append(
                                urwid.Text([attr[1], str(user[attr[0]])]))
                        index += 2
                    self.attr_list.body.extend(ready_extend_list)

            else:
                pass
        request=httpclient.HTTPRequest(api.user_init_info, 'GET', headers={
                                       'Cookie': global_values.token})
        httpclient.AsyncHTTPClient().fetch(request, resp_user_info)

class MainPanel(urwid.Frame):
    def __init__(self):
        body=urwid.Columns(
            [UserInfoPanel(), urwid.Text('功能面板'), urwid.Text('日志')])
        footer=urwid.Text('--状态栏--')
        super(MainPanel, self).__init__(urwid.ListBox(urwid.SimpleFocusListWalker(
            [body])), footer=urwid.AttrMap(footer, 'status_bar'))

class LoginPanel(urwid.WidgetPlaceholder):
    def __init__(self):
        def on_login_result(response: httpclient.HTTPResponse):
            if response.code == 200:
                json_rst=json.loads(response.body)
                if 'code' in json_rst and json_rst['code'] == 200:
                    global_values.token=response.headers['Set-Cookie'].split(';')[0]
                    self.original_widget=MainPanel()
                else:
                    self.login_result_info.set_text('登录失败')
        def login(button):
            uname=self.uname_edit.get_edit_text()
            pwd=self.pwd_edit.get_edit_text()
            request=httpclient.HTTPRequest(
                api.login, 'POST', body='user_name={}&user_pwd={}'.format(uname, pwd))
            httpclient.AsyncHTTPClient().fetch(request, on_login_result)
        super(LoginPanel, self).__init__(urwid.SolidFill(' '))
        logo=urwid.Text('')
        with open('./logo.txt') as logo_file:
            logo.set_text(logo_file.read())
        self.uname_edit=urwid.Edit('账号: ')
        self.pwd_edit=urwid.Edit('密码: ', mask='*')
        login_btn=urwid.Button('登陆', on_press=login)
        login_btn_wp=urwid.Padding(
            login_btn, align=urwid.CENTER, width=('relative', 18))
        self.login_result_info=urwid.Text('', align=urwid.CENTER)
        form=urwid.LineBox(urwid.Pile([self.uname_edit, self.pwd_edit, urwid.AttrMap(
            self.login_result_info, 'error_info'), login_btn_wp]))
        self.original_widget=urwid.Overlay(
            urwid.ListBox(urwid.SimpleFocusListWalker([logo, form])),
            self.original_widget,
            align='center', width=45,
            valign='middle', height=('relative', 80),
            min_width=24, min_height=8,
            left=10, right=10,
            top=5,
            bottom=5)


if __name__ == '__main__':
    main_panel=LoginPanel()
    loop=urwid.TornadoEventLoop(IOLoop())
    urwid.MainLoop(main_panel, palette=global_values.palette,
                   event_loop=loop).run()

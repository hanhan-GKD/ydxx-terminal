import urwid
import tornado
from tornado.ioloop import IOLoop

class LoginPanel(urwid.WidgetPlaceholder):
    def __init__(self):
        super(LoginPanel, self).__init__(urwid.SolidFill(' '))
        logo = urwid.Text('')
        with open('./logo.txt') as logo_file:
            logo.set_text(logo_file.read())
        uname_edit = urwid.Edit('账号: ')
        pwd_edit = urwid.Edit('密码: ', mask='*')
        login_btn = urwid.Button('登陆')
        login_btn_wp = urwid.Padding(login_btn, align=urwid.CENTER, width=('relative', 18))
        form = urwid.LineBox(urwid.Pile([uname_edit, pwd_edit, login_btn_wp]))
        self.original_widget = urwid.Overlay(
            urwid.ListBox(urwid.SimpleFocusListWalker([logo, form])),
            self.original_widget,
            align='center', width=45,
            valign='middle', height=('relative', 80),
            min_width=24, min_height=8,
            left=10, right=10,
            top=5,
            bottom=5)


def main():
    login_panel = LoginPanel()
    loop = urwid.TornadoEventLoop(IOLoop())
    urwid.MainLoop(login_panel, event_loop=loop).run()
if __name__ == '__main__':
    main()

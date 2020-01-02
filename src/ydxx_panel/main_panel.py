import urwid
from src.api import api
from src.global_values import global_values
from src.ydxx_widget import button
from src.ydxx_widget import menu_widget
from src.ydxx_panel.userinfo_panel import UserInfoPanel

class MainPanel(urwid.Frame):

    def __init__(self):
        body = menu_widget.MenuWidget([('角色信息', UserInfoPanel()), ('背包', urwid.Text('背包: 空'))])

        footer = urwid.Text('--状态栏--')
        super(MainPanel, self).__init__(urwid.ListBox(urwid.SimpleFocusListWalker(
            [body])), footer=urwid.AttrMap(footer, 'status_bar'))


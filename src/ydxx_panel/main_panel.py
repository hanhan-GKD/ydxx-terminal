import urwid
from src.globals.api import api
from src.globals.global_values import global_values
from src.ydxx_widget.menu import MenuWidget
from src.ydxx_panel.userinfo_panel import UserInfoPanel
from src.ydxx_panel.team_adventure_panel import TeamAdventurePanel

class MainPanel(urwid.Frame):

    def __init__(self):
        body = MenuWidget([('角色信息', UserInfoPanel()),
                                       ('组队冒险', TeamAdventurePanel())])

        footer = urwid.Text('--状态栏--')
        super(MainPanel, self).__init__(urwid.ListBox(urwid.SimpleFocusListWalker(
            [body])), footer=urwid.AttrMap(footer, 'status_bar'))
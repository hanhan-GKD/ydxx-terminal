#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
主界面
"""
import urwid

from src.ydxx_panel.settings_panel import SettingsPanel
from src.ydxx_panel.team_adventure_panel import TeamAdventurePanel
from src.ydxx_panel.userinfo_panel import UserInfoPanel
from src.ydxx_widget.menu import MenuWidget


class MainPanel(urwid.Frame):

    def __init__(self):
        body = MenuWidget(
            [
                ('角色信息', UserInfoPanel()),
                ('组队冒险', TeamAdventurePanel()),
                ('系统设置', SettingsPanel()),
            ]
        )

        footer = urwid.Text('--状态栏--')
        super(MainPanel, self).__init__(
            urwid.ListBox(
                urwid.SimpleFocusListWalker([body])
            ),
            footer=urwid.AttrMap(footer, 'status_bar')
        )

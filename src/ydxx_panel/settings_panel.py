#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
退出菜单
"""
import asyncio

import urwid

from src.globals.api import api
from src.globals.global_values import global_values
from src.ydxx_widget import menu
from src.ydxx_widget.button import Button


class SettingsPanel(menu.MenuWidgetItem):
    """
    退出
    """

    def __init__(self):

        def exit_button(button):
            """
            退出按钮
            """
            raise urwid.ExitMainLoop()

        def logout_button(button):
            asyncio.get_event_loop().create_task(self.logout_api())

        exit_button = Button("退出程序", on_press=exit_button)
        logout_button = Button("退出登录", on_press=logout_button)
        form = urwid.ListBox(
            urwid.SimpleFocusListWalker(
                [
                    exit_button,
                    logout_button,
                ]
            )
        )
        super(SettingsPanel, self).__init__(form)

    @staticmethod
    async def logout_api():
        """
        退出登录
        """
        from src.ydxx_panel.login_panel import LoginPanel

        async with global_values.session.post(api.logout):
            global_values.top.original_widget = LoginPanel()

#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import asyncio

import urwid

from src.globals.global_values import global_values
from src.ydxx_panel.login_panel import LoginPanel


if __name__ == '__main__':
    main_panel = urwid.WidgetPlaceholder(LoginPanel())
    global_values.top = main_panel
    urwid.MainLoop(
        main_panel,
        palette=global_values.palette,
        event_loop=urwid.AsyncioEventLoop(
            loop=asyncio.get_event_loop()
        )
    ).run()

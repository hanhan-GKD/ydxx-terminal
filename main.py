#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import urwid
import asyncio
from src.ydxx_panel.login_panel import LoginPanel
from src.globals.global_values import global_values


if __name__ == '__main__':
    main_panel = LoginPanel()
    urwid.MainLoop(main_panel, palette=global_values.palette,
                   event_loop=urwid.AsyncioEventLoop(loop=asyncio.get_event_loop())).run()

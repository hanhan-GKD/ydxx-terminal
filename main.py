#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import urwid
from tornado.ioloop import IOLoop
from src.ydxx_panel.login_panel import LoginPanel
from src.global_values import global_values



if __name__ == '__main__':
    main_panel = LoginPanel()
    loop = urwid.TornadoEventLoop(IOLoop())
    urwid.MainLoop(main_panel, palette=global_values.palette,
                   event_loop=loop).run()

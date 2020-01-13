#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
from typing import Callable

import urwid


class Button(urwid.WidgetWrap):
    signals = ['click']
    """
    按钮按下时会发射click信号， 使用urwid.connect_signal来绑定绑定处理函数
    :param text: 按钮显示的内容
    :param on_press: 按钮按下时的回调函数, 建议使用urwid.connect_signal来绑定回调函数
    :param user_data: 按钮按下时传递给回调函数额外的参数
    :param highlight: 按钮成为焦点时的display_attribute
    """
    def __init__(self, text, on_press: Callable = None, user_data: any = None, highlight: str = None): 
        self.label = urwid.SelectableIcon(text, cursor_position=len(text) + 2)
        if not highlight:
            highlight = 'active_button'
        super(Button, self).__init__(urwid.AttrMap(self.label, None, focus_map=highlight))
        if on_press:
            urwid.connect_signal(self, 'click', on_press, user_data)

    def keypress(self, size, key):
        if self._command_map[key] != urwid.ACTIVATE:
            return key
        self._emit('click')

    def mouse_event(self, size, event, button, x, y, focus):
        if button != 1 or not urwid.util.is_mouse_press(event):
            return False
        self._emit('click')
        return True
    

#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import urwid
from src.ydxx_widget.button import Button


class MenuListBox(urwid.ListBox):
    signals = ['change_focus']

    def change_focus(self, size, position,
                     offset_inset=0, coming_from=None,
                     cursor_coords=None, snap_rows=None):
        super(MenuListBox, self).change_focus(size, position,
                                              offset_inset, coming_from,
                                              cursor_coords, snap_rows)
        self._emit('change_focus', position)


class MenuEmptyError(Exception):

    def __init__(self):
        super(MenuEmptyError, self).__init__('cannot init MenuWidget with a empty list')


class MenuWidget(urwid.Columns):
    def __init__(self, menu_list: [(str, urwid.Widget)]):
        if len(menu_list) < 1:
            raise MenuEmptyError()
        self.body_list = []
        self.menu_items = []
        self.position = 0
        for (title, body) in menu_list:
            self.menu_items.append(Button(title, highlight='active_menu_item'))
            self.body_list.append(body)
        self.menu = MenuListBox(urwid.SimpleFocusListWalker(self.menu_items))
        urwid.connect_signal(self.menu, 'change_focus', lambda x, position: self.switch_menu_item(position))
        super(MenuWidget, self).__init__([(12, self.menu), urwid.WidgetPlaceholder(self.body_list[0])], box_columns=[0])

    def switch_menu_item(self, position):
        if position != self.position and position in range(0, len(self.body_list)):
            self.position = position
            self.widget_list[1].original_widget = self.body_list[position]

    def keypress(self, size, key):
        if self.focus_position == 0:
            if key == 'enter':
                self.set_focus(1)
            elif self._command_map[key] not in ('cursor left', 'cursor right'):
                return super(MenuWidget, self).keypress(size, key)
        else:
            return super(MenuWidget, self).keypress(size, key)



class MenuWidgetItem(urwid.WidgetWrap):
    def __init__(self, widget: urwid.Widget):
        if urwid.FLOW in widget.sizing():
            super(MenuWidgetItem, self).__init__(widget)
        elif urwid.BOX in widget.sizing():
            super(MenuWidgetItem, self).__init__(urwid.BoxAdapter(widget, 23))

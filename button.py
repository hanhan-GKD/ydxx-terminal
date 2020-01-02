import urwid
from typing import Callable
from global_values import global_values

class Button(urwid.WidgetWrap):
    signals = ['click']
    def __init__(self, text, on_press: Callable = None, user_data=None, highlight:str = None):
        self.label = urwid.SelectableIcon(text)
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
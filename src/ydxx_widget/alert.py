import urwid
from src.globals.global_values import global_values
from src.ydxx_widget.button import Button
from typing import Callable

class Alert:
    YES = 0x1
    NO = 0x2
    YES_NO = 0x3

class AlertError(Exception):
    pass



"""
:param widget   弹出框中展示的内容widget
:param header   弹出框标题
:param callback 用户选择确定或取消后执行回调函数, 函数返回True时将关闭弹出框
:raises AlertError: widget不是urwid.Widget类型或无法确认widget的高度时将引发AlertError
"""
def alert(widget, header:str = '', callback: Callable[[int], bool] = None, style: int = Alert.YES):
    def _on_click(Button, click):
        if not callback or callback and callback(click):
            global_values.top.original_widget = global_values.top.original_widget[0]

    if style == Alert.YES_NO:
        btns = [('pack', Button('确认', on_press=_on_click, user_data=Alert.YES)),
                ('pack', Button('取消', on_press=_on_click, user_data=Alert.NO))]
    else:
        btns = [urwid.Padding(Button(
            '确认', on_press=_on_click, user_data=Alert.YES), align=urwid.CENTER, width='pack')]
    if hasattr(widget, 'rows'):
        if urwid.FLOW in widget.sizing():
            height = widget.rows((10, ))
        elif urwid.BOX in widget.sizing():
            height = widget.rows((10, 40))
        else:
            raise AlertError('cannot determine {} height, either FLOW or BOX defined'.format(widget))
    elif hasattr(widget, 'pack'):
        (height, ) = widget.pack()
    else:
        raise AlertError('cannot determine {} height, either rows() or pack() defined'.format(widget))
    height += 6

    alert_widget = urwid.LineBox(urwid.ListBox(urwid.SimpleFocusListWalker(
        [urwid.Text(header), urwid.Divider('-'), widget, urwid.Divider(' '), urwid.Columns(btns, dividechars=30)])))
    global_values.top.original_widget = urwid.Overlay(
        alert_widget, global_values.top.original_widget, 
        'center', 40, 'middle', height)

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
:param widget:   弹出框中展示的内容widget
:param header :  弹出框标题
:param callback: 用户选择确定或取消后执行回调函数, 函数返回True时将关闭弹出框
:raises AlertError: widget不是urwid.Widget类型或无法确认widget的高度时将引发AlertError
"""
def alert(widget, header:str = '', callback: Callable[[int], bool] = None, style: int = Alert.YES):
    def _on_click(Button, click):
        if not callback or callback and callback(click):
            global_values.top.original_widget = global_values.top.original_widget[0]
    top = global_values.top
    if isinstance(top.original_widget, urwid.Overlay):
        top_w = top.original_widget.top_w
        if hasattr(top_w, 'attr_map'):
            attr_map = top_w.attr_map
            if attr_map.get('is_alert'):
                top.original_widget = global_values.top.original_widget[0]

    if style == Alert.YES_NO:
        btns = [urwid.Padding(Button('确认', on_press=_on_click, user_data=Alert.YES), width='pack', left=10),
                urwid.Padding(Button('取消', on_press=_on_click, user_data=Alert.NO), align=urwid.RIGHT, width='pack', right=10)]
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
        [urwid.Text(header), urwid.Divider('-'), widget, urwid.Divider(' '), urwid.Columns(btns)])))
    top.original_widget = urwid.Overlay(
        urwid.AttrMap(alert_widget, {'is_alert': True}), top.original_widget,
        'center', 40, 'middle', height)

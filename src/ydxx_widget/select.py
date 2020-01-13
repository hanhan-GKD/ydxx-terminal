import urwid
from typing import List, Tuple

class Select(urwid.WidgetWrap):
    left = '<'
    right = '>'
    signals = ['select_change']
    """
    Select组件选项发生改变时， 会发射select_change信号。
    用户按下enter键将Select组件选中为焦点。
    仅当Select组件被设置为焦点才会响应 up、down、left、right等用户输入来改变选中内容。
    :param data: Select初始化数据
    :param cap: 未选择时显示的内容
    :param auto_select: 自动选中为焦点
    :param highlight: 组建选中为焦点时的display_attribute
    """
    def __init__(self, data: List[Tuple[str, any]], cap: str = '选择', auto_select: bool = True, highlight = 'select_focus'):
        self.index = -1 
        self.data = data
        self.select_label = urwid.SelectableIcon(cap, cursor_position=20)
        self.auto_select = auto_select
        self.select = auto_select
        self.highlight = highlight
        self.left_pair = urwid.Text(self.left)
        self.right_pair = urwid.Text(self.right)
        self._highlight(auto_select)
        super(Select, self).__init__(urwid.Columns(
            [('pack', self.left_pair), ('pack', self.select_label), ('pack', self.right_pair)]))
    
    def keypress(self, size, key):
        if self.select:
            if key == 'enter':
                self._highlight(False)
                self.select = False
            elif key == 'left' or key == 'up':
                length = len(self.data)
                if length == 0:
                    return
                if self.index < 0:
                    new_index = self.index + length
                else:
                    new_index = (self.index - 1) % length
                self._change(new_index)
            elif key == 'right' or key == 'down':
                length = len(self.data)
                if length == 0:
                    return
                new_index = ( self.index + 1 ) % length
                self._change(new_index)
            elif key == 'ctrl right':
                return 'right'
            elif key == 'ctrl down':
                return 'down'
            elif key == 'ctrl up':
                return 'up'
            elif key == 'ctrl left':
                return 'left'
        else:
            if key == 'enter' or self.auto_select:
                self.select = True
                self._highlight(True)
            return super(Select, self).keypress(size, key)

    def _change(self, index):
        if index != self.index:
            self.index = index
            data = self.data[self.index]
            self._emit('select_change', data)
            self.select_label.set_text(data[0])
            
    def _highlight(self, focus):
        if focus:
            self.left_pair.set_text((self.highlight, self.left))
            self.right_pair.set_text((self.highlight, self.right))
        else:
            self.left_pair.set_text(self.left)
            self.right_pair.set_text(self.right)

    def value(self):
        if(self.index < 0):
            return None
        return self.data[self.index][1]
    
    def set_data(self, data):
        self.data = data

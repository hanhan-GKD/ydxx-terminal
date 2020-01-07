import urwid
from typing import List, Tuple

class Select(urwid.WidgetWrap):
    left = '◀'
    right = '▶'
    signals = ['select_change']
    """
    Select组件选项发生改变时， 会发射select_change信号
    :param data Select初始化数据， 默认选中第一个选项
    """
    def __init__(self, data: List[Tuple[str, any]], cap: str = '选择'):
        self.index = -1 
        self.data = data
        self.select_label = urwid.SelectableIcon(cap)
        super(Select, self).__init__(urwid.Columns(
            [(2, urwid.Text(self.left)), ('pack', self.select_label), ('pack', urwid.Text(self.right))]))
    
    def keypress(self, size, key):
        if key == 'enter' or key == 'ctrl right':
            new_index = ( self.index + 1 ) % len(self.data)
            self._change(new_index)
        elif key == 'ctrl left':
            if self.index < 0: 
                new_index = self.index + len(self.data)
            else:
                new_index = (self.index - 1) % len(self.data)
            self._change(new_index)
        else:
            return super(Select, self).keypress(size, key)

    def _change(self, index):
        if index != self.index:
            self.index = index
            data = self.data[self.index]
            self._emit('select_change', data)
            self.select_label.set_text(data[0])

    def value(self):
        if(self.index < 0):
            return None
        return self.data[self.index]
    
    def set_data(self, data):
        self.data = data
        self.select_label.set_text(self.data[self.index][0])

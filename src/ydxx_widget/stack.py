import urwid
from typing import List
import abc


"""
StackWidget中存放的Widget内容
"""
class StackFrame(urwid.WidgetWrap):
    signals = ['exit']
    """
    子类必须实现此函数，显示当前Frame的标题
    """
    @abc.abstractmethod
    def title(self):
        pass
    
    """
    StackWidget将Frame切换到在后台时将回调此函数
    """
    def on_foreground(self):
        pass

    """
    StackWidget将Frame切换到在前台时将回调此函数
    """
    def on_background(self):
        pass
    
    """
    StackWidget将Frame放入stack中时将回调此函数
    """
    def on_entry(self):
        pass

    """
    StackWidget将Frame移出stack中时将回调此函数
    """
    def on_leave(self):
        pass

    def exit(self):
        self._emit('exit')

class StackWidget(urwid.WidgetWrap):
    """
    
    :param widget_list: 放入stack中的列表
    """
    def __init__(self, widget_list: List[StackFrame]):
        self.widget_list = widget_list
        self.header = urwid.Text('', align=urwid.CENTER)
        if len(self.widget_list) > 0:
            self.body = urwid.WidgetPlaceholder(self.widget_list[-1])
            self.index = len(self.widget_list) - 1
            self.header.set_text(self.widget_list[-1].title())
        else:
            self.body = urwid.WidgetPlaceholder(None)
            self.index = -1
        for w in self.widget_list:
            urwid.connect_signal(w, 'exit', self.exit_frame)
        super(StackWidget, self).__init__(urwid.Pile([self.header, self.body]))

    def keypress(self, size, key):
        if self.index > 0 and key == 'esc':
            self.pop()
        else:
            return super(StackWidget, self).keypress(size, key)
    
    def push(self, widget: StackFrame):
        self.index += 1
        self.widget_list.append(widget)
        self.body.original_widget.on_background()
        widget.on_entry()
        self.body.original_widget = widget
        self.header.set_text(widget.title())
        urwid.connect_signal(widget, 'exit', self.exit_frame)

    def pop(self):
        urwid.disconnect_signal(self.body.original_widget, 'exit', self.exit_frame)
        self.index -= 1
        new_body = self.widget_list[self.index]
        self.body.original_widget.on_leave()
        new_body.on_foreground()
        self.body.original_widget = new_body
        self.header.set_text(new_body.title())
        self.widget_list.remove(self.widget_list[-1])
 
    def exit_frame(self, w):
        self.pop()
import urwid
from typing import List
import abc


class StackFrame(urwid.WidgetWrap):
    @abc.abstractmethod
    def title(self):
        pass
    
    def on_foreground(self):
        pass

    def on_background(self):
        pass
    
    def on_entry(self):
        pass

    def on_leave(self):
        pass

class StackWidget(urwid.WidgetWrap):
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

    def pop(self):
        self.index -= 1
        new_body = self.widget_list[self.index]
        self.body.original_widget.on_leave()
        new_body.on_foreground()
        self.body.original_widget = new_body
        self.header.set_text(new_body.title())
        self.widget_list.remove(self.widget_list[-1])
 
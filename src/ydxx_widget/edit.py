import urwid

class IntEdit(urwid.Edit):
    """
    扩展urwid.Edit, 实现IntEdit。
    :param edit_text: 输入框默认内容
    :max: 用户可输入的最大数据
    """
    def __init__(self, edit_text: int = 0, max: int = -1):
        self.max = max
        super(IntEdit, self).__init__(edit_text=str(edit_text))
    def valid_char(self, ch):
        if len(ch) == 1 and ch in "0123456789":
            try:
                if self.max > 0:
                    char_list = list(self.text)
                    char_list.insert(self.edit_pos, ch)
                    return int(''.join(char_list)) <= self.max
                else:
                    return True
            except ValueError as err:
                print(err)
        return False

    def set_edit_text(self, text):
        if text:
            text = self._normalize_to_caption(str(int(text)))
        self.highlight = None
        self._emit("change", text)
        old_text = self._edit_text
        self._edit_text = text
        if self.edit_pos > len(text):
            self.edit_pos = len(text)
        self._emit("postchange", old_text)
        self._invalidate()

    """
    :return 返回输入框中的数据
    """
    def value(self):
        if self.edit_text:
            return int(self.edit_text)
        else:
            return 0

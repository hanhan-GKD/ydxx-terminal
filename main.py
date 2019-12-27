#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import urwid


def main():
    txt = urwid.Text(u"hello world")
    fill = urwid.Filler(txt, "middle")
    loop = urwid.MainLoop(fill)
    loop.run()


if __name__ == '__main__':
    main()

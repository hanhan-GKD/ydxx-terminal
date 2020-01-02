#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-


class GlobalContainer(object):
    """
    全局容器？
    """

    def __init__(self):
        self._values = {}

    def __getattribute__(self, key):
        if key == '_values':
            return object.__getattribute__(self, '_values')
        return object.__getattribute__(self, '_values')[key]

    def __setattr__(self, name, value):
        if name != '_values':
            self._values[name] = value
        else:
            object.__setattr__(self, name, value)

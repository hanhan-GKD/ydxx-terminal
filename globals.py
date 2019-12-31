class GlobalContainer():
    def __init__(self):
        self._values = {}
    def __getattribute__(self, key):
        if key == '_values':
            return object.__getattribute__(self, '_values')
        try:
            return object.__getattribute__(self, '_values')[key]
        except KeyError:
            return None
    def __setattr__(self, name, value):
        if name != '_values':
            self._values[name] = value
        else:
            object.__setattr__(self, name, value)
import gc


class BaseConstant:
    def __init__(self, name, value=None, display_name=None):
        self._name = name
        self._value = value
        self._display_name = display_name

    @classmethod
    def get_constants(cls):
        """"""
        for obj in gc.get_objects():
            if isinstance(obj, cls):
                yield obj

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def display_name(self):
        if self._display_name:
            return self._display_name
        return self.name

    @display_name.setter
    def display_name(self, value):
        self._display_name = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

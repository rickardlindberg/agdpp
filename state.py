class ResettableValue:

    """
    >>> i = ResettableValue(5)
    >>> i.get_and_reset()
    5
    >>> i.set(6)
    >>> i.get_and_reset()
    6
    >>> i.get_and_reset()
    5
    """

    def __init__(self, default):
        self.default = default
        self.value = default

    def get_and_reset(self):
        x = self.get()
        self.reset()
        return x

    def get(self):
        return self.value

    def set(self, value):
        self.value = value

    def reset(self):
        self.value = self.default

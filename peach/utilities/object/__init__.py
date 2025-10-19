class PartiallyPacked:
    """
    Utility to return the first value of a tuple by default, unless otherwise unpacked.
    """

    def __init__(self, *values):
        self.values = values

    def __iter__(self):
        return iter(self.values)

    def __repr__(self):
        return repr(self.values[0])

    def __str__(self):
        return str(self.values[0])

    def __int__(self):
        return int(self.values[0])

    def __float__(self):
        return float(self.values[0])

    def __bool__(self):
        return bool(self.values[0])

    def __getattr__(self, name):
        return getattr(self.values[0], name)

    def __call__(self):
        return self.values[0]

    def __getitem__(self, index):
        return self.values[index]

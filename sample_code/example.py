"""Sample file with a couple of undocumented functions, used to test the scanner."""


def add_numbers(a, b):
    return a + b


def find_max(values):
    result = values[0]
    for v in values[1:]:
        if v > result:
            result = v
    return result


class Counter:
    def __init__(self, start=0):
        self.count = start

    def increment(self, step=1):
        self.count += step
        return self.count

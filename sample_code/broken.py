"""Deliberately broken Python fixture.
 
This file does NOT parse. It exists so the scanner can be tested against
invalid input -- it should be skipped with a warning, not crash the scan.
Do not "fix" it.
"""
 
 
def add_numbers(a, b)
    return a + b
 
 
class Counter:
    def __init__(self, start=0):
        self.count = start
----------------------------------------------------------------------------------------------------

add_numbers [Function] (lines: 4-5):


Adds two numbers together.

Args:
    a (int or float): The first number to add.
    b (int or float): The second number to add.

Returns:
    int or float: The sum of a and b.


----------------------------------------------------------------------------------------------------

find_max [Function] (lines: 8-13):


Finds the maximum value in a list of numbers.

Args:
    values (list of int or float): A list of numbers.

Returns:
    int or float: The maximum value found in the list.

Raises:
    ValueError: If the list is empty.


----------------------------------------------------------------------------------------------------

Counter [Class] (lines: 16-22):


A simple counter class.

Args:
    start (int, optional): The initial value of the counter. Defaults to 0.

Methods:
    increment(step=1): Increments the counter by a specified step.

    Args:
        step (int, optional): The amount to increment the counter by. Defaults to 1.


----------------------------------------------------------------------------------------------------

__init__ [Function] (lines: 17-18):


Initializes the counter with a given start value.

Args:
    start (int, optional): The initial value of the counter. Defaults to 0.

Attributes:
    count (int): The current value of the counter.


----------------------------------------------------------------------------------------------------

increment [Function] (lines: 20-22):


Increments the count by a specified step.

Args:
    step (int, optional): The amount to increment the count by. Defaults to 1.

Returns:
    int: The updated count after incrementing.

Raises:
    None


----------------------------------------------------------------------------------------------------


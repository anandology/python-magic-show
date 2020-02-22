"""
Python Magic Show Trick: Print in Reverse

How to Use:
    
    $ export PYTHONSTARTUP=path/to/rprint.py
    $ python
    >>> for i in range(10): print(i+1)
    ...
    1
    2
    3
    4
    5
    6
    7
    8
    9
    01
"""
real_print = print

def print(*args, **kwargs):
    """Magic print to print all the numbers in reverse order.
    """
    args = [ulta(a) for a in args]
    real_print(*args, **kwargs)

def ulta(x):
    """Reverses the argument if it is a number.
    """
    if isinstance(x, int):
        return str(x)[::-1]
    else:
        return x

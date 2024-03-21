def is_even(num: int) -> bool:
    """Return True if num is even.
    >>> is_even(2)
    True
    >>> is_even(3)
    True
    """
    return num % 2 == 0


if __name__ == '__main__':
    import doctest

    doctest.testmod()

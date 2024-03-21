from __future__ import annotations
from typing import List, Optional, TextIO
import json


def play_next(num: str) -> str:
    """
    >>> play_next("haha")
    'haha'
    """
    return num


class Try:
    pass


if __name__ == '__main__':
    """    
    with open('input_files/config_642_05.json', 'r') as f:
        lines = f.read().splitlines()
    print(lines)
    print(lines[0])
    print(lines[1][19: -1])
    print(lines[2][19: -1])
    print(lines[3][22: -1])
    print(lines[4][19:])
    """
    import doctest
    doctest.testmod()
    play_next(8)
    #
    # list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    #
    # print(list[2:4 + 6:8])
    # a = 8
    # for i in range(0, a):
    #     print("hhh")

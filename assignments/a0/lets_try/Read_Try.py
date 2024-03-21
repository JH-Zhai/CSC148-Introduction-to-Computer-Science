from __future__ import annotations
from typing import List, Dict, TextIO, Optional

SENTINEL = 'END_REPLIES'


def read_cheeps(f: TextIO) -> None:
    lines = f.read().splitlines()
    print(lines)


if __name__ == '__main__':

    with open('D:/cheep_data.txt') as f:
        read_cheeps(f)


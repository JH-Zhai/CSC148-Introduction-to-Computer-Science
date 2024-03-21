"""CSC148 Assignment 1: Tests for GroceryStore

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains starter code for testing the GroceryStore class.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""
from io import StringIO
from store import GroceryStore

# TODO: write your test functions for GroceryStore here
# Note - your tests should use StringIO to simulate opening a configuration file
# rather than requiring separate files.
# See the Assignment 0 sample test for an example of using StringIO in testing.

CONFIG_F = '''{
  "regular_count": 10,
  "express_count": 20,
  "self_serve_count": 4,
  "line_capacity": 2
}
'''


def test_read_config() -> None:
    store = GroceryStore(StringIO(CONFIG_F))
    regular_count = 10
    express_count = 20
    self_serve_count = 4
    line_capacity = 2
    for i in range(regular_count + express_count + self_serve_count):
        assert store.line_is_ready(i) == True
        assert store.get_first_in_line(i) == None
        store.close_line(i)
        assert store.line_is_ready(i) == False


if __name__ == '__main__':
    import pytest
    pytest.main(['test_grocerystore.py'])

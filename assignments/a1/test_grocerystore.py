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
from store import GroceryStore, Customer, Item

# Note - your tests should use StringIO to simulate opening a configuration file
# rather than requiring separate files.
# See the Assignment 0 sample test for an example of using StringIO in testing.

CONFIG_F1 = '''{
  "regular_count": 10,
  "express_count": 20,
  "self_serve_count": 4,
  "line_capacity": 2
}
'''

def test_read_config() -> None:
    store = GroceryStore(StringIO(CONFIG_F1))
    regular_count = 10
    express_count = 20
    self_serve_count = 4
    for i in range(regular_count + express_count + self_serve_count):
        assert store.line_is_ready(i) is False
        assert store.get_first_in_line(i) is None
        store.close_line(i)
        assert store.line_is_ready(i) is False
        # assert store._checkout_lines[i].capacity == 2
    # assert len(store._checkout_lines) == 34


def test_enter_line_and_line_is_ready() -> None:
    store = GroceryStore(StringIO(CONFIG_F1))
    regular_count = 10
    express_count = 20
    self_serve_count = 4

    c = Customer('David', [Item('toy', 3)])
    d = Customer('Leo', [Item('pencil', 5)])
    for i in range(regular_count + express_count + self_serve_count):
        assert store.enter_line(c) == i
        assert store.line_is_ready(i) is True
    assert store.enter_line(d) == 0
    assert store.line_is_ready(0) is False
    store.complete_checkout(0)
    assert store.line_is_ready(0) is True
    assert store.get_first_in_line(0) is d
    store.complete_checkout(0)
    assert store.get_first_in_line(0) is None
    store.close_line(1)
    assert store.line_is_ready(1) is True
    assert store.enter_line(d) == 0
    assert store.enter_line(d) == 0
    assert store.enter_line(d) == 2


if __name__ == '__main__':
    import pytest
    pytest.main(['test_grocerystore.py'])

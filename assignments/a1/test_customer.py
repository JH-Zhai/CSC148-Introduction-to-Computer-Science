"""CSC148 Assignment 1: Tests for Customer

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains starter code for testing the Customer class.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""
from store import Customer, Item

def test_arrival_time() -> None:
    c = Customer('David', [])
    assert c.name == 'David'
    assert c.arrival_time == -1
    assert c.num_items() == 0

def test_num_item() -> None:
    c = Customer('David', \
                 [Item('Computer', 100), Item('Phone', 10), Item('Laptop', 1)])
    assert c.num_items() == 3
    d = Customer('David', [])
    assert d.num_items() == 0

def test_many_num_item() -> None:
    item_lst = []
    for i in range(999):
        item_lst.append(Item(f'Item {i}', i))
    c = Customer('David', item_lst)
    assert c.num_items() == 999

def test_get_item_time() -> None:
    c = Customer('Violet',\
                 [Item('Letter', 100), Item('Pen', 10), Item('Ink', 1)])
    assert c.get_item_time() == 111

def test_many_get_item_time() -> None:
    item_lst = []
    for i in range(1, 1000):
        item_lst.append(Item(f'Letter {i}', i))
    c = Customer('Violet', item_lst)
    assert c.get_item_time() == 499500

if __name__ == '__main__':
    import pytest
    pytest.main(['test_customer.py'])

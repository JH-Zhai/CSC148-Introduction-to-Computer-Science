"""CSC148 Assignment 1: Tests for checkout classes

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains starter code for testing the checkout classes.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""
from store import RegularLine, ExpressLine, SelfServeLine, Customer, Item

# TODO: write your test functions for the checkout classes here

def test_empty_line_len() -> None:
    rl = RegularLine(1)
    el = ExpressLine(1)
    ssl = SelfServeLine(1)
    assert len(rl) == 0
    assert len(el) == 0
    assert len(ssl) == 0

def test_open_after_close() -> None:
    c = Customer('David', [])
    rl = RegularLine(1)
    el = ExpressLine(1)
    ssl = SelfServeLine(1)
    assert rl.can_accept(c) == True
    assert el.can_accept(c) == True
    assert ssl.can_accept(c) == True
    rl.close()
    el.close()
    ssl.close()
    assert rl.can_accept(c) == False
    assert el.can_accept(c) == False
    assert ssl.can_accept(c) == False

def test_checkout() -> None:
    c = Customer('David', [])
    rl = RegularLine(1)
    el = ExpressLine(1)
    ssl = SelfServeLine(1)
    rl.accept(c)
    el.accept(c)
    ssl.accept(c)
    assert rl.start_checkout() == 0
    assert el.start_checkout() == 0
    assert ssl.start_checkout() == 0
    assert rl.complete_checkout() == False
    assert el.complete_checkout() == False
    assert ssl.complete_checkout() == False

def test_customer_with_many_items() -> None:
    item_lst = []
    for i in range(1, 1000):
        item_lst.append(Item(f'Letter {i}', i))
    c = Customer('Violet', item_lst)
    rl = RegularLine(1)
    el = ExpressLine(1)
    ssl = SelfServeLine(1)
    assert rl.accept(c) == True
    assert el.accept(c) == False
    assert ssl.accept(c) == True

if __name__ == '__main__':
    import pytest
    pytest.main(['test_checkouts.py'])

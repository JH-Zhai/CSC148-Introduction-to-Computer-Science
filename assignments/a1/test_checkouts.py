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
    assert rl.can_accept(c) is True
    assert el.can_accept(c) is True
    assert ssl.can_accept(c) is True
    rl.close()
    el.close()
    ssl.close()
    assert rl.can_accept(c) is False
    assert el.can_accept(c) is False
    assert ssl.can_accept(c) is False

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
    assert rl.complete_checkout() is False
    assert el.complete_checkout() is False
    assert ssl.complete_checkout() is False
    c = Customer('David', [Item('toy', 3)])
    d = Customer('Leo', [Item('pencil', 5)])
    rl = RegularLine(2)
    el = ExpressLine(2)
    ssl = SelfServeLine(2)
    rl.accept(c)
    el.accept(c)
    ssl.accept(c)
    rl.accept(d)
    el.accept(d)
    ssl.accept(d)
    assert rl.start_checkout() == 3
    assert el.start_checkout() == 3
    assert ssl.start_checkout() == 6
    assert rl.complete_checkout() is True
    assert el.complete_checkout() is True
    assert ssl.complete_checkout() is True
    assert rl.start_checkout() == 5
    assert el.start_checkout() == 5
    assert ssl.start_checkout() == 10
    assert rl.complete_checkout() is False
    assert el.complete_checkout() is False
    assert ssl.complete_checkout() is False

def test_customer_with_many_items() -> None:
    item_lst = []
    for i in range(1, 1000):
        item_lst.append(Item(f'Letter {i}', i))
    c = Customer('Violet', item_lst)
    rl = RegularLine(1)
    el = ExpressLine(1)
    ssl = SelfServeLine(1)
    assert rl.accept(c) is True
    assert el.accept(c) is False
    assert ssl.accept(c) is True
    d = Customer('Violet', [Item('toy', 4)])
    assert rl.can_accept(d) is False
    assert el.can_accept(d) is True
    assert ssl.can_accept(d) is False
    assert rl.accept(d) is False
    assert el.accept(d) is True
    assert ssl.accept(d) is False

if __name__ == '__main__':
    import pytestf
    pytest.main(['test_checkouts.py'])

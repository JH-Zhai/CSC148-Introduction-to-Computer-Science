"""CSC148 Prep 5: Linked Lists

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Prep 5.

You must fill in the body of the test case test_to_list().

WARNING: THIS IS AN EXTREMELY INCOMPLETE SET OF TESTS!
Add your own to practice writing tests and to be confident your code is correct.
"""
from typing import List
from prep5 import LinkedList, _Node

def test_to_list() -> None:
    """Test LinkedList.to_list"""
    # provided you, but so that it passes on a correct implementation
    # (like the one in the course notes.)
    lst = LinkedList()
    node1 = _Node(1)
    node2 = _Node(None)
    node3 = _Node(3)
    node1.next = node2
    node2.next = node3
    lst._first = node1
    assert lst.to_list() == [1, None, 3]

# ------------------------------------------------------------------------
# The below are sample tests for you to test your code on.
# We highly recommend that you write your own test cases to test your
# code!
# ------------------------------------------------------------------------
def test_len_empty() -> None:
    """Test LinkedList.__len__ for an empty linked list."""
    lst = LinkedList()
    assert len(lst) == 0




def test_len_not_empty() -> None:
    """Test LinkedList.__len__ for a not empty linked list."""
    lst = LinkedList()
    node1 = _Node(1)
    lst._first = node1
    assert len(lst) == 1


def test_len_three() -> None:
    """Test LinkedList.__len__ on a linked list of length 3."""
    lst = LinkedList()
    node1 = _Node(10)
    node2 = _Node(20)
    node3 = _Node(30)
    node1.next = node2
    node2.next = node3
    lst._first = node1

    assert len(lst) == 3


def test_contains_doctest() -> None:
    """Test LinkedList.__contains__ on the given doctest."""
    lst = LinkedList()
    node1 = _Node(1)
    node2 = _Node(2)
    node3 = _Node(3)
    node1.next = node2
    node2.next = node3
    lst._first = node1

    assert 2 in lst
    assert not (4 in lst)


def test_append_empty() -> None:
    """Test LinkedList.append on an empty list."""
    lst = LinkedList()
    lst.append(1)
    assert lst._first.item == 1


def test_append_one() -> None:
    """Test LinkedList.append on a list of length 1."""
    lst = LinkedList()
    lst._first = _Node(1)
    lst.append(2)
    assert lst._first.next.item == 2


if __name__ == '__main__':
    import pytest
    pytest.main(['prep5_sample_test.py'])

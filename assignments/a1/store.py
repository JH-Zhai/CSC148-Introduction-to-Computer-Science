"""CSC148 Assignment 1 - Modelling a Grocery Store (Task 1a)

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains all of the classes necessary to model the entities
in a grocery store.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""
from __future__ import annotations
from typing import List, Optional, TextIO
import json

# Use this constant in your code
EXPRESS_LIMIT = 7


# You may add private attributes and helper methods, but do not change the
# public interface.
# Write docstrings for all methods you write, and document your attributes
# in the class docstring.
class GroceryStore:
    """A grocery store.

    === Attributes ===
    _regular_count: number of regular line
    _express_count: number of express line
    _self_serve_count: number of self serve line
    _line_capacity: max customer in on line
    _checkout_lines: list of all checkout lines
    """
    _regular_count: int
    _express_count: int
    _self_serve_count: int
    _line_capacity: int
    _checkout_lines: List

    def __init__(self, config_file: TextIO) -> None:
        """Initialize a GroceryStore from a configuration file <config_file>.
        """
        self._checkout_lines = []
        file = json.load(config_file)
        self._regular_count = file['regular_count']

        self._express_count = file['express_count']

        self._self_serve_count = file['self_serve_count']

        self._line_capacity = file['line_capacity']

        for _ in range(self._regular_count):
            line = RegularLine(self._line_capacity)
            self._checkout_lines.append(line)
        for _ in range(self._express_count):
            line = ExpressLine(self._line_capacity)
            self._checkout_lines.append(line)
        for _ in range(self._self_serve_count):
            line = SelfServeLine(self._line_capacity)
            self._checkout_lines.append(line)

    def enter_line(self, customer: Customer) -> int:
        """Pick a new line for <customer> to join.

        Return the index of the line that the customer joined.
        Must use the algorithm from the handout.

        Return -1 if there is no line available for the customer to join.
        """
        index_of_available_lines = []
        for i in range(len(self._checkout_lines)):
            if self._checkout_lines[i].can_accept(customer):
                index_of_available_lines.append(i)
        if not index_of_available_lines:
            return -1
        number_of_people_in_line = \
            len(self._checkout_lines[index_of_available_lines[0]].queue)

        return_value = index_of_available_lines[0]
        for j in index_of_available_lines:
            if len(self._checkout_lines[j].queue) < number_of_people_in_line:
                return_value = j
                number_of_people_in_line = len(self._checkout_lines[j].queue)
        self._checkout_lines[return_value].accept(customer)
        return return_value

    def line_is_ready(self, line_number: int) -> bool:
        """Return True iff checkout line <line_number>
        is ready to start a checkout.
        """
        ready = False
        if len(self._checkout_lines[line_number].queue) == 1:
            ready = True
        return ready

    def start_checkout(self, line_number: int) -> int:
        """Return the time it will take to check out the next customer in
        line <line_number>
        """
        return self._checkout_lines[line_number].start_checkout()

    def complete_checkout(self, line_number: int) -> bool:
        """Return True iff there are customers remaining to be checked out in
        line <line_number>
        """

        return self._checkout_lines[line_number].complete_checkout()

    def close_line(self, line_number: int) -> List[Customer]:
        """Close checkout line <line_number> and return the customers from
        that line who are still waiting to be checked out.
        """
        if line_number >= len(self._checkout_lines):
            return []
        return self._checkout_lines[line_number].close()

    def get_first_in_line(self, line_number: int) -> Optional[Customer]:
        """Return the first customer in line <line_number>, or None if there
        are no customers in line.
        """
        if self._checkout_lines[line_number].queue:
            return self._checkout_lines[line_number].queue[0]
        return None


# You should use the existing attributes in your solution. However, if you need
# to, you may add private attributes and helper methods, but do not change the
# public interface.
# Write docstrings for all methods you write, and document your attributes
# in the class docstring.
class Customer:
    """A grocery store customer.

    === Attributes ===
    name: A unique identifier for this customer.
    arrival_time: The time this customer joined a line.
    _items: The items this customer has.

    === Representation Invariant ===
    arrival_time >= 0 if this customer has joined a line, and -1 otherwise
    """
    name: str
    arrival_time: int
    _items: List[Item]

    def __init__(self, name: str, items: List[Item]) -> None:
        """Initialize a customer with the given <name>, an initial arrival time
         of -1, and a copy of the list <items>.

        >>> item_list = [Item('bananas', 7)]
        >>> belinda = Customer('Belinda', item_list)
        >>> belinda.name
        'Belinda'
        >>> belinda._items == item_list
        True
        >>> belinda.arrival_time
        -1
        """
        self.name = name
        self.arrival_time = -1
        self._items = items

    def num_items(self) -> int:
        """Return the number of items this customer has.

        >>> c = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
        >>> c.num_items()
        2
        """
        return len(self._items)

    def get_item_time(self) -> int:
        """Return the number of seconds it takes to check out this customer.

        >>> c = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
        >>> c.get_item_time()
        10
        """
        total_time = 0
        for item in self._items:
            total_time += item.get_time()
        return total_time


class Item:
    """A class to represent an item to be checked out.

    Do not change this class.

    === Attributes ===
    name: the name of this item
    _time: the amount of time it takes to checkout this item
    """
    name: str
    _time: int

    def __init__(self, name: str, time: int) -> None:
        """Initialize a new time with <name> and <time>.

        >>> item = Item('bananas', 7)
        >>> item.name
        'bananas'
        >>> item._time
        7
        """
        self.name = name
        self._time = time

    def get_time(self) -> int:
        """Return how many seconds it takes to checkout this item.

        >>> item = Item('bananas', 7)
        >>> item.get_time()
        7
        """
        return self._time


# Do not add any new attributes or methods (public or private) to this class.
class CheckoutLine:
    """A checkout line in a grocery store.

    This is an abstract class; subclasses are responsible for implementing
    start_checkout().

    === Attributes ===
    capacity: The number of customers allowed in this CheckoutLine.
    is_open: True iff the line is open.
    queue: Customers in this line in FIFO order.

    === Representation Invariants ===
    - Each customer in this line has not been checked out yet.
    - The number of customers is less than or equal to capacity.
    """
    capacity: int
    is_open: bool
    queue: List[Customer]

    def __init__(self, capacity: int) -> None:
        """Initialize an open and empty CheckoutLine.

        >>> line = CheckoutLine(1)
        >>> line.capacity
        1
        >>> line.is_open
        True
        >>> line.queue
        []
        """
        self.capacity = capacity
        self.is_open = True
        self.queue = []

    def __len__(self) -> int:
        """Return the size of this CheckoutLine.
        """
        return len(self.queue)

    def can_accept(self, customer: Customer) -> bool:
        """Return True iff this CheckoutLine can accept <customer>.
           This is a abstract function
        """
        return len(self.queue) < self.capacity and self.is_open

    def accept(self, customer: Customer) -> bool:
        """Accept <customer> at the end of this CheckoutLine.
        Return True iff the customer is accepted.

        >>> line = CheckoutLine(1)
        >>> c1 = Customer('Belinda', [Item('cheese', 3)])
        >>> c2 = Customer('Hamman', [Item('chips', 4), Item('gum', 1)])
        >>> line.accept(c1)
        True
        >>> line.accept(c2)
        False
        >>> line.queue == [c1]
        True
        """
        if self.can_accept(customer):
            self.queue.append(customer)
            return True
        return False

    def start_checkout(self) -> int:
        """Checkout the next customer in this CheckoutLine.
        Return the time it will take to checkout the next customer.
        """
        return self.queue[0].get_item_time()

    def complete_checkout(self) -> bool:
        """Finish the checkout for this CheckoutLine.

        Return whether there are any remaining customers in the line.
        """
        self.queue.pop(0)

        return len(self.queue) > 0

    def close(self) -> List[Customer]:
        """Close this line.

        Return a list of all customers that need to be moved to another line.
        """
        self.is_open = False
        a = self.queue.copy()
        if self.queue:
            self.queue = [self.queue[0]]
            a.pop(0)

        return a


# Only implement those methods that cannot be used exactly as inherited
# from the superclass.
# You may add private attributes and helper methods, but do not change the
# public interface of the subclasses.
# Write docstrings for all methods you write, and document your attributes
# in the class docstring.

class RegularLine(CheckoutLine):
    """A regular CheckoutLine."""


class ExpressLine(CheckoutLine):
    """An express CheckoutLine.
    """

    def can_accept(self, customer: Customer) -> bool:
        """Return True iff this CheckoutLine can accept <customer>.
           This is a abstract function
        """
        return CheckoutLine.can_accept(self, customer) and \
               customer.num_items() <= EXPRESS_LIMIT


class SelfServeLine(CheckoutLine):
    """A self-serve CheckoutLine.
    """

    def can_accept(self, customer: Customer) -> bool:
        """Return True iff this CheckoutLine can accept <customer>.
           This is a abstract function
        """
        return len(self.queue) < self.capacity and self.is_open

    def start_checkout(self) -> int:
        """Checkout the next customer in this CheckoutLine.
        Return the time it will take to checkout the next customer.
        """
        return 2 * CheckoutLine.start_checkout(self)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': ['__future__', 'typing', 'json',
                                   'python_ta', 'doctest'],
        'disable': ['W0613']})

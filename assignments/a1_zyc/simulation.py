"""Assignment 1 - Grocery Store Simulation (Task 3)

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains a class to simulate a grocery store, as well as some
example testing code.

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
from typing import Dict, Any, TextIO
from event import create_event_list, CustomerArrival, CheckoutCompleted
from store import GroceryStore
from container import PriorityQueue


class GroceryStoreSimulation:
    """A Grocery Store simulation.

    This is the class which is responsible for setting up and running a
    simulation. The interface is given to you: your main task is to implement
    the two methods according to their docstrings.

    Of course, you may add whatever private attributes you want to this class.
    Because you should not change the interface in any way, you may not add
    any public attributes.

    === Private Attributes ===
    _events: A sequence of events arranged in priority determined by the event
             sorting order.
    _store: The store being simulated.
    """
    _events: PriorityQueue
    _store: GroceryStore

    def __init__(self, store_file: TextIO) -> None:
        """Initialize a GroceryStoreSimulation using configuration <store_file>.
        """
        self._events = PriorityQueue()
        self._store = GroceryStore(store_file)

    def run(self, file: TextIO) -> Dict[str, Any]:
        """Run the simulation on the events stored in <initial_events>.

        Return a dictionary containing statistics of the simulation,
        according to the specifications in the assignment handout.
        """
        # Initialize statistics
        stats = {
            'num_customers': 0,
            'total_time': 0,
            'max_wait': -1
        }
        # TODO: Calculate and return the correct statistics.
        event_lst = create_event_list(file)
        event_add_lst = []
        for event in event_lst:
            self._events.add(event)
        cus_dict = {}
        cus_cnt = 0
        while not self._events.is_empty():
            event = self._events.remove()
            # print(f'{type(event)} @ {event.timestamp}')
            event_add_lst = event.do(self._store)
            if isinstance(event, CustomerArrival):
                if event.customer.name not in cus_dict:
                    cus_dict[event.customer.name] = 1
                    cus_cnt += 1
            elif isinstance(event, CheckoutCompleted):
                stats['max_wait'] = \
                    max(stats['max_wait'], \
                        event.timestamp - event.customer.arrival_time)
            stats['total_time'] = max(stats['total_time'], event.timestamp)
            for event_add in event_add_lst:
                self._events.add(event_add)
        stats['num_customers'] = cus_cnt
        return stats


# We have provided a bit of code to help test your work.
if __name__ == '__main__':
    config_file = open('input_files/config_111_01.json')
    # config_file = open('input_files/config_100_01.json')
    sim = GroceryStoreSimulation(config_file)
    config_file.close()
    event_file = open('input_files/events_one.txt')
    # event_file = open('input_files/events_two.txt')
    sim_stats = sim.run(event_file)
    event_file.close()
    print(sim_stats)
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['__future__', 'typing', 'event', 'store',
                                   'container', 'python_ta', 'doctest']})

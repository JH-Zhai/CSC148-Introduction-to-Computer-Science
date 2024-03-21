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
        input_events = create_event_list(file)
        for event in input_events:
            self._events.add(event)
        total_time = 0
        num_customers = 0
        max_wait = 0
        wait_time = {}
        while not self._events.is_empty():
            event = self._events.remove()

            if isinstance(event, CustomerArrival):
                if event.customer.name not in wait_time.keys():
                    wait_time.update({event.customer.name: event.timestamp})

            if isinstance(event, CheckoutCompleted):
                num_customers += 1
                if (event.timestamp - wait_time[event.customer.name]) > \
                        max_wait:
                    max_wait = event.timestamp - wait_time[event.customer.name]

            new_events = event.do(self._store)

            for new_event in new_events:
                self._events.add(new_event)
            if self._events.is_empty():
                total_time = event.timestamp

        stats['num_customers'] = num_customers
        stats['total_time'] = total_time
        stats['max_wait'] = max_wait

        return stats


# We have provided a bit of code to help test your work.
if __name__ == '__main__':
    config_file = open('input_files/config_111_01.json')
    sim = GroceryStoreSimulation(config_file)
    config_file.close()
    event_file = open('input_files/events_one.txt')
    sim_stats = sim.run(event_file)
    event_file.close()
    print(sim_stats)
    import doctest

    doctest.testmod()
    import python_ta

    python_ta.check_all(config={'allowed-import-modules': ['__future__',
                                                           'typing', 'event',
                                                           'store', 'container',
                                                           'python_ta',
                                                           'doctest']})

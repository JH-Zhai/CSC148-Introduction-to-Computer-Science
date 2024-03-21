"""CSC148 Assignment 1: Sample tests

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Assignment 1.

Warning: This is an extremely incomplete set of tests!

Note: this file is to only help you; you will not submit it when you hand in
the assignment.

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
from simulation import GroceryStoreSimulation
import json

CONFIG_FILE = '''{
  "regular_count": 1,
  "express_count": 0,
  "self_serve_count": 0,
  "line_capacity": 1
}
'''

EVENT_FILE = '''10 Arrive Tamara Bananas 7
5 Arrive Jugo Bread 3 Cheese 3
'''

CONFIG_FILE_NAME = ['config_001_10.json', 'config_010_10.json', \
                    'config_100_01.json', 'config_100_10.json', \
                    'config_111_01.json', 'config_111_10.json', \
                    'config_300_01.json', 'config_300_10.json', \
                    'config_333_01.json', 'config_333_10.json', \
                    'config_642_05.json']

EVENT_FILE_NAME = [ \
    'events_base.txt', 'events_mixtures.txt', 'events_no_express.txt', \
    'events_one_at_a_time.txt', 'events_one_close.txt', 'events_one.txt', \
    'events_two.txt' ]



if __name__ == '__main__':
    # print("Hi")
    # gss = GroceryStoreSimulation(open(f'./input_files/{CONFIG_FILE_NAME[0]}'))
    # stats = gss.run(open(f'./input_files/{EVENT_FILE_NAME[0]}'))
    # print(f'{CONFIG_FILE_NAME[0]} {EVENT_FILE_NAME[0]}: {stats}')
    # print(open(f'./input_files/{EVENT_FILE_NAME[0]}').read().count('Close'))

    for config_f in CONFIG_FILE_NAME:
        for event_f in EVENT_FILE_NAME:
            jsonObject = json.load(open(f'./input_files/{config_f}'))
            regular_count = jsonObject['regular_count']
            express_count = jsonObject['express_count']
            self_serve_count = jsonObject['self_serve_count']
            if open(f'./input_files/{event_f}').read().count('Close') < regular_count + express_count + self_serve_count:
                if config_f == 'config_010_10.json' and event_f == 'events_no_express.txt':
                    continue
                print(f'{config_f} {event_f}:')
                # gss = GroceryStoreSimulation(open(f'./input_files/{config_f}'))
                # stats = gss.run(open(f'./input_files/{event_f}'))
                config_file = open(f'./input_files/{config_f}')
                sim = GroceryStoreSimulation(config_file)
                config_file.close()
                event_file = open(f'./input_files/{event_f}')
                sim_stats = sim.run(event_file)
                event_file.close()
                # print(sim_stats)
                print(f'{sim_stats}\n')


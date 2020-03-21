#!/usr/bin/env python

# this file is part of the github repository: https://github.com/nwhoppe/nanobody_fitness
# author: nwhoppe
# created: 3/17/20

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""script to make a random training and test set from two input """)
    required = parser.add_argument_group('required')
    args = parser.parse_args()
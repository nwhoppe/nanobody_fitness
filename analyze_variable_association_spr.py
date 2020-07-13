#!/usr/bin/env python3

import argparse
import pandas as pd


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""script 
    align dissociation phase
    normalize max at start of dissociation
    keep zero zero
    fit single exponential with rate constant constrained across samples
    plot raw curves - # do last
    """)
    required = parser.add_argument_group('required')
    required.add_argument('-s', '--sensorgram_raw_data', required=True, nargs='*',
                          help='raw txt from Biacore T100 machine of reference subtracted sensorgram')
    parser.add_argument()
    args = parser.parse_args()

    # cycle number is unfortunately the header and not time, so going to manually assign
    # columns alternate x and y; x is time and 0 starts association

    sensorgram_df_list = []
    for raw_sensorgram_data in args.s:
        

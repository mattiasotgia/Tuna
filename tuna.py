#!/usr/bin/env python3


import tuna
import json

import sys, os
import argparse


if __name__ == '__main__':
    sys.stdout.write(tuna.NAME)
    sys.stdout.write(f'Developed by {tuna.AUTHOR} <{tuna.MAIL}>\nRelase {tuna.VERSION} ({tuna.RELASE_DATE})\n\n')
    cliapp = argparse.ArgumentParser('tuna')
    
    # Arguments
    cliapp.add_argument('-c', '--configuration', action='store', required=True)
    cliapp.add_argument('-v', '--verbose', action='store', 
                        required=False, nargs='?', const='2', default='2', 
                        choices=['0', '1', '2'], help='Verbosity level 0: ERRORS, 1: WARNINGS, 2: INFO')

    args = cliapp.parse_args()
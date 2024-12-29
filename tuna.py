#!/usr/bin/env python3


import tuna
import json

import sys, os
import argparse
import logging

from tuna.helpers import create_logger

if __name__ == '__main__':

    cliapp = argparse.ArgumentParser('tuna')
    
    # Arguments
    cliapp.add_argument('-c', '--configuration', action='store', required=True)
    cliapp.add_argument('-b', '--batch', action='store_true', default=False, help='Run in batch mode (no splash screen)')
    # cliapp.add_argument('-v', '--verbose', action='store', 
    #                     required=False, nargs='?', const='2', default='0', 
    #                     choices=['0', '1', '2'], help='Verbosity level 0: ERRORS, 1: WARNINGS, 2: INFO. Default to 0: ERRORS')

    args = cliapp.parse_args()

    if not args.batch:
        sys.stdout.write(tuna.version.NAME)
        sys.stdout.write(f'Developed by {tuna.version.AUTHOR} <{tuna.MAIL}>\nRelase {tuna.VERSION} ({tuna.RELASE_DATE})\n\n')


    configuration = tuna.config(args.configuration)
    if configuration:
        configuration.run()


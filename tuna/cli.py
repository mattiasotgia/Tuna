#!/usr/bin/env python3

# from __future__ import annotations

import argparse
import logging
import sys

import tuna.version
from tuna.utils.helpers import config, create_logger

def main():
    '''Main cli interface for the tuna-cli program
    This is called by the cli command tuna -c CONFIGURATION [-h] [-v] [-V VERBOSE] [-b]
    Installation and documentation on README.md or page'''

    cliapp = argparse.ArgumentParser('tuna')
    
    # Arguments
    cliapp.add_argument('-c', '--configuration', action='store')
    cliapp.add_argument('-b', '--batch', action='store_true', default=False, help='Run in batch mode (no splash screen)')
    cliapp.add_argument('-v', '--version', action='store_true', 
                        help='Show version and important info of the TUNA cliapp. If called with -c will show the versioning of all modules called by the configuration file'
                        )
    cliapp.add_argument('-V', '--verbose', action='store', 
                        required=False, nargs='?', const='2', default='0', 
                        choices=['0', '1', '2'], help='Verbosity level 0: ERRORS, 1: WARNINGS, 2: INFO. Default to 0: ERRORS')

    args = cliapp.parse_args()

    create_logger(__name__, True, level=(logging.INFO if args.verbose == '2' else (logging.WARNING if args.verbose == '1' else logging.ERROR)))

    if not args.configuration and not args.version:
        create_logger(__name__).error('Provide -c CONFIGURATION, -v or -v -c CONFIGURATION please. Help with -h')

    if not args.batch:
        sys.stdout.write(tuna.version.NAME)
        
    if args.version:
        sys.stdout.write(f'Developed by {tuna.version.AUTHOR} <{tuna.version.MAIL}>\nRelase {tuna.version.VERSION} ({tuna.version.RELASE_DATE})\n\n')

    if args.configuration:
        configuration = config(args.configuration)
            
        if configuration:
            configuration.run(args.version)


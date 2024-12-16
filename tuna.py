#!/usr/bin/env python3


import tuna
import json

import sys, os
import argparse
import logging

if __name__ == '__main__':

    cliapp = argparse.ArgumentParser('tuna')
    
    # Arguments
    cliapp.add_argument('-c', '--configuration', action='store', required=True)
    cliapp.add_argument('-b', '--batch', action='store_true', default=False, help='Run in batch mode (no splash screen)')
    cliapp.add_argument('-v', '--verbose', action='store', 
                        required=False, nargs='?', const='2', default='0', 
                        choices=['0', '1', '2'], help='Verbosity level 0: ERRORS, 1: WARNINGS, 2: INFO. Default to 0: ERRORS')

    args = cliapp.parse_args()

    if not args.batch:
        sys.stdout.write(tuna.version.NAME)
        sys.stdout.write(f'Developed by {tuna.version.AUTHOR} <{tuna.MAIL}>\nRelase {tuna.VERSION} ({tuna.RELASE_DATE})\n\n')

    logger = logging.getLogger('TUNA')
    logger.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    console.setLevel(
        logging.INFO if args.verbose == '2' else (logging.WARNING if args.verbose == '1' else logging.ERROR)
    )

    logfile = logging.FileHandler('tuna.log')
    logfile.setLevel(logging.INFO)

    console.setFormatter(logging.Formatter('[%(name)s: %(levelname)s] %(message)s'))
    logfile.setFormatter(logging.Formatter('[%(asctime)s - %(name)s] %(levelname)s: %(message)s'))

    logger.addHandler(console)
    logger.addHandler(logfile)


    try:
        with open(args.configuration, 'r') as conf:
           configuration = json.load(conf)

    except FileNotFoundError:
        logger.error(f'The file \'{args.configuration}\' was not found.')
        sys.exit()
    except PermissionError:
        logger.error('You do not have permission to access this file.')
        sys.exit()
    except Exception as e:
        logger.error(f'An unexpected error occurred: {e}')
        sys.exit()

    logger.info(f'Loaded configuration {args.configuration} with {len(configuration.keys())} keys')



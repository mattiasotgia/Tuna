#!/usr/bin/env python3

from __future__ import annotations

import argparse


if __name__ == '__main__':

    cliapp = argparse.ArgumentParser('tuna')
    
    # Arguments
    cliapp.add_argument('-c', '--configuration', action='store')
    cliapp.add_argument('-b', '--batch', action='store_true', default=False, help='Run in batch mode (no splash screen)')
    cliapp.add_argument('-v', '--version', action='store_true', help='Show version and important info of the TUNA cliapp. If called with -c will show the versioning of all modules called by the configuration file') #! TODO: implementare questa funzione
    # cliapp.add_argument('-v', '--verbose', action='store', 
    #                     required=False, nargs='?', const='2', default='0', 
    #                     choices=['0', '1', '2'], help='Verbosity level 0: ERRORS, 1: WARNINGS, 2: INFO. Default to 0: ERRORS')

    args = cliapp.parse_args()

    if not args.batch:
        sys.stdout.write(tuna.version.NAME)
        
    if args.version:
        sys.stdout.write(f'Developed by {tuna.version.AUTHOR} <{tuna.MAIL}>\nRelase {tuna.VERSION} ({tuna.RELASE_DATE})\n\n')

    if args.configuration:
        configuration = tuna.config(args.configuration)
        if configuration:
            configuration.run()


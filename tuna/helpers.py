'''Helper functions/classes for the TUNA package
'''

from __future__ import annotations

import importlib
import json
import sys, os

from io import TextIOWrapper
from typing import Any
import logging

# from tuna.modules import Module

def create_logger(name: Any) -> logging.Logger:
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        console = logging.StreamHandler()
        console.setFormatter(logging.Formatter(':::: %(name)s: %(levelname)s :::: \n%(message)s'))
        logger.addHandler(console)

    return logger


class ModuleConfiguration:

    def __init__(self, module_configuration: dict, subroutine_name: str):
        module_name: str | None = None
        try:
            module_name = module_configuration['module_name']
        except KeyError: 
            create_logger(__name__).error(
                'Not able to load the module_name key for subroutine %s, perhaps it is missing?',
                subroutine_name
            )
        except Exception as e:
            create_logger(__name__).error(e)

        self.module_name = module_name

    def get(self, index, default = None):
        pass

    def __getitem__(self, index):
        pass

class Configuration:

    def __init__(self):
        self.subroutines = []
        self.name = 'unknown'
        self.__init_config__: dict = {}
        self.path = ''

    def __str__(self) -> str:
        return f'tuna.helpers.Configuration \'{self.name}\' ({len(self.subroutines)} subroutines)'

    def load(self, configuration: dict | TextIOWrapper | str):
        create_logger(__name__).info('Loaded configuration')

        if isinstance(configuration, str):
            try: 
                tmp = json.load(open(configuration))
            except Exception as e:
                create_logger(__name__).error(e)
        elif isinstance(configuration, TextIOWrapper):
            tmp = json.load(configuration)
        else:
            tmp = configuration

        self.__init_config__: dict = tmp

        try:
            self.name = tmp['name']
        except KeyError:
            create_logger(__name__).error('Processed configuration but missing name, autoassigning')
        except Exception as e:
            create_logger(__name__).error(e)


        self.subroutines = list(tmp.keys() - ['name'])
        self.path = tmp.get('modules_path', 'tuna.modules')

    def run(self) -> None:
        '''Run the current configuration. 
        '''
        create_logger(__name__).info('Running %s', self)

        for sr in self.subroutines:
            create_logger(__name__).info('Running subroutine %s\nThe subroutine configuration follows', sr)

            module_conf = ModuleConfiguration(self.__init_config__.get(sr, {}), sr)

            ## Run the actual modules inside the configuration files
            #  1. Import the module path
            if not module_conf.module_name:
                create_logger(__name__).warning(
                    'Stopped execution of subroutine %s, no module_name was provided', 
                    sr
                )
                continue
            
            if isinstance(module_conf.module_name, str):
                try: 
                
                    module_path_imported = importlib.__import__(
                        f'{self.path}.{module_conf.module_name}',
                        globals(), locals(),
                        [module_conf.module_name]
                    )
                except ModuleNotFoundError:
                    create_logger(__name__).warning(
                        'Whilist module_name was provided, no module found in %s, under the name %s', 
                        f'{self.path}.{module_conf.module_name}', module_conf.module_name
                    )
                except Exception as e:
                    create_logger(__name__).error(e)
                
                module = eval(f'module_path_imported.{module_conf.module_name}()')
                module(module_conf)



def config(
    configuration_file: str | TextIOWrapper | None = None,
):
    '''Create configuration from file path/TextIOWrapper

    Return
    ------
    `None` or `tuna.helper.Configuration` 
    '''
    configuration = Configuration()
    if configuration_file is None:
        create_logger(__name__).error('No configuration file provided. Aborting. ')
        return None

    elif isinstance(configuration_file, str):
        try:
            with open(configuration_file) as reader:
                create_logger(__name__).info('Created configuration from file %s',
                                             configuration_file)
                configuration.load(reader)
        except Exception as e:
            create_logger(__name__).error(e)

    elif isinstance(configuration_file, TextIOWrapper):
        create_logger(__name__).info('Created configuration from TextIOWrapper')
        configuration.load(configuration_file)
    return configuration

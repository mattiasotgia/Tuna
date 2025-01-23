'''Helper functions/classes for the TUNA package
'''

# from __future__ import annotations

import logging
import importlib
import json

from io import TextIOWrapper
import sys
from typing import Any


def create_logger(name: Any, main = False, level = logging.INFO) -> logging.Logger:
    '''Simple utility to create instantaeous logger (using basic configuration)'''

    logger = logging.getLogger(name)

    if main:
        logging.basicConfig(
            level=level,
            format='[%(name)s: %(levelname)s] %(message)s',
            # format='%(levelname)s: %(message)s',
            handlers=[
                logging.StreamHandler()
            ]
        )
    return logger


class ModuleConfiguration:
    '''Loader for configuration in the single modules 
    '''

    def __init__(self, module_configuration: dict[str, Any], subroutine_name: str | None = None):
        self.module_name: str | None = module_configuration.pop('module_name', None)
        self.module_import_path: str | None =  module_configuration.pop(
            'module_import_path', self.module_name
        )
        self.configuration = module_configuration
        self.base_configuration = {}
        self.__default__ = False

        if subroutine_name and not self.module_name:
            create_logger(__name__).error(
                'Missing "module_name" key for subroutine "%s".', subroutine_name
            )

    
    def get(self, key: str, required: bool = False):
        '''Retrieve a configuration key with optional requirement check'''

        default_value = None

        if not self.__default__:
            required = True
        else:
            try:
                default_value = self.base_configuration[key]
            except KeyError:
                create_logger(__name__).error(
                    'No key %s found on the base configuration even though base_configuration exists \nThis would break so killing the process...',
                    key
                )
                sys.exit(2)

        try:
            value = self.configuration[key]
        except KeyError:
                if required:
                    create_logger(__name__).error(
                        'Key %s is required, so the program will not work.',
                        key
                    )
                    sys.exit(2)
                else:
                    value = self.configuration.get(key, default_value)

        return value

    def default(self, default_config_path: str):
        '''Set default configuration for module. Call this 
        first time the module itself is built (in the `Module.update()` function)
        
        Internally sets `self.__default__ = False` if file not opened/json loader not parsed. 
        '''
        self.__default__ = True

        try:
            with open(default_config_path) as f:
                self.base_configuration = json.load(f)
        
        except FileNotFoundError:
            create_logger(__name__).warning('Base configuration not found, \n [?] %s', default_config_path)
            self.__default__ = False
        except json.JSONDecodeError as e:
            create_logger(__name__).warning(
                'Failed to parse JSON from %s: %s', default_config_path, e
            )
            self.__default__ = False
        
    def __getitem__(self, key):
        '''Get configuration key with fallback to default'''
        return self.configuration.get(key, self.base_configuration.get(key))
    
    def __str__(self) -> str:
        
        description_module = f'\n:::::::: Configuration for module tuna.modules.{self.module_import_path}.{self.module_name} \n'
        for key in self.configuration.keys():
            description_module += f' ** {key}: {self.configuration[key]} (type: {type(self.configuration[key])})\n'
        if not self.configuration.keys():
            description_module += f' ** EMPTY configuration for module...\n'
        description_module += ':::::::: PROLOG END \n'
        return description_module

class Configuration:
    '''Configuration class'''

    def __init__(self):
        self.subroutines: list[str] = []
        self.name = 'unknown'
        self.path = 'tuna.modules'
        self.initial_configuration: dict[str, Any] = {}

    def __str__(self) -> str:
        return f"{__name__}.Configuration(name='{self.name}' subroutines={self.subroutines})"

    def load(self, configuration: dict | str | TextIOWrapper):
        '''Load the cofiguration from either a `str` path, a `TextIOWrapper` or a `json` loader `dict`

        Parameters
        ----------
        `configuration`: `dict`, `TextIOWrapper` or `str`
            Configuration file to load
        
        Return
        ------
        `Configuration`: `self`
        '''

        if isinstance(configuration, str):
            try:
                with open(configuration) as f:
                    tmp = json.load(f) 
            except FileNotFoundError:
                create_logger(__name__).error(
                    'The file corresponding to the configuration loaded is not existing\nPath %s not found',
                    configuration
                )
            except json.JSONDecodeError as e:
                create_logger(__name__).error(
                    'Reading configuration there were some error in json parsing\nPath %s\nJSON decoding error follows: %s',
                    configuration, e
                )
        elif isinstance(configuration, TextIOWrapper):
            try:
                tmp = json.load(configuration)
            except json.JSONDecodeError as e:
                create_logger(__name__).error(
                    'Reading configuration there were some error in json parsing\nJSON decoding error follows: %s',
                    e
                )
        else:
            tmp = configuration

        self.initial_configuration = tmp

        self.name = tmp.pop('name', self.name)
        self.path = tmp.pop('modules_path', self.path)

        self.subroutines = list(tmp.keys())

        return self

    def run(self, version=False) -> None:
        '''Run the current configuration. 
        '''

        create_logger(__name__).info('Running %s', self)

        print(f'Found {len(self.subroutines)} subroutines in configuration named {self.name}')
        print('Running...    ><(((º>  \n')

        for idx, subroutine in enumerate(self.subroutines):

            print(f'[** {idx+1}] Running subroutine `{subroutine}`')

            module_conf = ModuleConfiguration(
                self.initial_configuration.get(subroutine, {}), subroutine
            )

            if not version:
                print(module_conf)

            ## Run the actual modules inside the configuration files
            #  1. Import the module path
            if not module_conf.module_name:
                create_logger(__name__).warning(
                    'Stopped execution of subroutine %s, no module_name was provided', 
                    subroutine
                )
                continue
            
            if isinstance(module_conf.module_name, str):
                try:
                    module_path_imported = importlib.import_module(
                        f'{self.path}.{module_conf.module_import_path}'
                    )
                except ModuleNotFoundError:
                    create_logger(__name__).warning(
                        'Whilist module_name was provided, no module found in %s, under the name %s. Skipping configuration...', 
                        f'{self.path}.{module_conf.module_import_path}', module_conf.module_name
                    )
                    continue
                except Exception as e:
                    create_logger(__name__).error(e)
                    continue
                if not hasattr(module_path_imported, module_conf.module_name):
                    create_logger(__name__).warning(
                        'Whilist module_name was provided, no <tuna.modules.Module> found in %s, under the name %s.\nSkipping configuration...', 
                        f'{self.path}.{module_conf.module_import_path}', module_conf.module_name
                    )
                    continue
                
                module = getattr(module_path_imported, module_conf.module_name)()
                if version:
                    print(module)
                else:
                    module(module_conf)




def config(
    configuration_file: str | TextIOWrapper | None = None,
):
    '''Create configuration from file path/TextIOWrapper

    Return
    ------
    `None` or `tuna.helper.Configuration` 
    '''

    if not configuration_file:
        create_logger(__name__).error('No configuration file provided. Aborting.')
        return None

    configuration = Configuration()
    try:
        configuration.load(configuration_file)
        create_logger(__name__).info('Configuration loaded from "%s".', configuration_file)
        return configuration
    except Exception as e:
        create_logger(__name__).error('Failed to load configuration: %s', e)
        return None


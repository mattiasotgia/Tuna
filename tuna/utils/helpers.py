'''Helper functions/classes for the TUNA package
'''

from __future__ import annotations

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
            format=':::: %(levelname)s START :::: \n %(name)s: %(message)s \n:::: %(levelname)s END   ::::',
            # format='%(levelname)s: %(message)s',
            handlers=[
                logging.StreamHandler()
            ]
        )
    return logger


class ModuleConfiguration:
    '''Loader for configuration in the single modules 
    '''

    def __init__(self, module_configuration: dict, subroutine_name = None):
        module_name: str | None = None
        self.__default__ = False


        if subroutine_name:

            try:
                module_name = module_configuration['module_name']
            except KeyError:
                create_logger(__name__).error(
                    'Not able to load the module_name key for subroutine %s, perhaps it is missing?',
                    subroutine_name
                )

            self.module_name = module_name

            try:
                module_import_path = module_configuration['module_import_path']
            except KeyError:
                create_logger(__name__).warning(
                    'The key module_import_path was not found, using module_name (%s) for both',
                    module_name
                )
                module_import_path = module_name
            
            self.module_import_path = module_import_path

            module_configuration.pop('module_name', None)
            module_configuration.pop('module_import_path', None)

        self.configuration = module_configuration
    
    def get(self, index, required = False):
        '''Key getter (wrapper for dict)'''

        if not self.__default__:
            required = True

        key_val = None
        try:
            default = self.base_configuration[index]
        except KeyError:
            create_logger(__name__).error('No key %s found on the base confguraion, stopping...', index)
            sys.exit(2)

        if required:
            try:
                key_val = self.configuration[index]
            except KeyError:
                create_logger(__name__).error('Key %s is required, so the program will not work')
                sys.exit(2)
        else:
            key_val = self.configuration.get(index, default)

        return key_val

    def default(self, default_config: str):
        '''Set default configuration for module. Call this 
        first time the module itself is built (in the `Module.update()` function)
        '''
        self.__default__ = True
        __def_conf_str__ = default_config
        try:
            __file_read__ = open(__def_conf_str__)
        except FileNotFoundError:
            create_logger(__name__).error('Base configuration not found, \n [?] %s', __def_conf_str__)
        except Exception as e:
            create_logger(__name__).error(e)
        
        self.base_configuration = json.load(__file_read__)

    def __getitem__(self, index):
        '''Key getter (wrapper for dicts with error catching) '''
        value = None
        try:
            value = self.configuration[index]
        except KeyError:
            create_logger(__name__).warning(
                'No key `%s` found in module configuration\nfor module tuna.modules.%s.%s',
                index, self.module_import_path, self.module_name
            )
         
        return value
    
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
        self.subroutines = []
        self.name = 'unknown'
        self.__init_config__: dict = {}
        self.path = ''

    def __str__(self) -> str:
        return f'tuna.helpers.Configuration \'{self.name}\' ({len(self.subroutines)} subroutines)'

    def load(self, configuration: dict | TextIOWrapper | str):
        '''Load the cofiguration from either a `str` path, a `TextIOWrapper` or a `json` loader `dict`

        Parameters
        ----------
        `configuration`: `dict`, `TextIOWrapper` or `str`
            Configuration file to load
        
        Return
        ------
        `Configuration`: `self`
        '''
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

        return self

    def run(self, version=False) -> None:
        '''Run the current configuration. 
        '''
        create_logger(__name__).info('Running %s', self)

        print(f'Found {len(self.subroutines)} subroutines in configuration named {self.name}')
        print('Running...    ><(((º>  \n')

        for idx, sr in enumerate(self.subroutines):
            create_logger(__name__).info('Running subroutine %s\nThe subroutine configuration follows', sr)
            print(f'[** {idx+1}] Running subroutine `{sr}`')

            module_conf = ModuleConfiguration(self.__init_config__.get(sr, {}), sr)

            if not version:
                print(module_conf)

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
                        f'{self.path}.{module_conf.module_import_path}',
                        globals(), locals(),
                        [module_conf.module_name]
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
                        'Whilist module_name was provided, no module found in %s, under the name %s. Skipping configuration...', 
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
    configuration = Configuration()
    if configuration_file is None:
        create_logger(__name__).error('No configuration file provided (something went wrong along the way...) \nAborting. ')
        return None

    if isinstance(configuration_file, str):
        try:
            with open(configuration_file) as reader:
                create_logger(__name__).info('Created configuration from file %s',
                                             configuration_file)
                configuration.load(reader)
        except Exception as e:
            create_logger(__name__).error('%s\nNo configuration file provided (something went wrong along the way...) \nAborting. ', e)
            return None

    elif isinstance(configuration_file, TextIOWrapper):
        create_logger(__name__).info('Created configuration from TextIOWrapper')
        configuration.load(configuration_file)
    return configuration

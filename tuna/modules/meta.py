from __future__ import annotations

from tuna.helpers import create_logger
from tuna.helpers import Configuration, ModuleConfiguration

from typing import Any


class Module:

    ## Versioning and stuff
    __author__ = 'M Sotgia'
    __mail__ = 'msotgia@ge.infn.it'
    __version__ = 'None'
    __date__ = 'never'

    def __init__(self):
        self.configuration = None


    def update(self):
        '''Main computation inside the module is done here. This is called by the TUNA exec'''
        pass

    def __call__(self, configuration: ModuleConfiguration | None = None) -> Any:
        if self.configuration is None:
            if configuration is not None:
                self.configuration = configuration
            else:
                create_logger(__name__).error(
                    'No configuration was passed when calling the module'
                )
        
        ## Call module main
        self.update()

    def __str__(self) -> str:
        ## Mainly storing version informations about the current module and/or important versioning stuff
        author = getattr(self.__class__, "__author__", "Unknown Author")
        mail = getattr(self.__class__, "__mail__", "unknown@example.com")
        version = getattr(self.__class__, "__version__", "0.0.0")
        date = getattr(self.__class__, "__date__", "Unknown Date")

        return f'Module {self.__class__.__module__}.{self.__class__.__name__}\n  Author {author} <{mail}>\n  Version {version}, relased {date}'

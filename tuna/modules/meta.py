from __future__ import annotations

from tuna.helpers import create_logger
from tuna.helpers import Configuration, ModuleConfiguration

from typing import Any


class Module:

    def __init__(self):
        self.configuration = None

    def __call__(self, configuration: ModuleConfiguration | None = None) -> Any:
        if self.configuration is None:
            if configuration is not None:
                self.configuration = configuration
            else:
                create_logger(__name__).error(
                    'No configuration was passed in the creation of the module, nor in its call.'
                )
        create_logger(__name__).info('Called generic module')

    def __str__(self) -> str:
        return ''

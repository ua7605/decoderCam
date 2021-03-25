from enum import Enum


class Startup(Enum):
    CONFIG_FILE = 1
    CONFIG_FILE_CHECK = 2
    CONFIG_FILE_FAILURE = 3
    CONFIG_FILE_SUCCESS = 4

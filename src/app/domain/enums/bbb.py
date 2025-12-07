from enum import Enum


class ReturnCode(str, Enum):
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'

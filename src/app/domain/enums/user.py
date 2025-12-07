from enum import Enum


class UserRole(str, Enum):
    MODERATOR = 'moderator'
    VIEWER = 'viewer'

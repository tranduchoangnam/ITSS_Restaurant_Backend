from enum import Enum


class AccountStatus(Enum):
    active = "active"
    suspended = "suspended"
    deleted = "deleted"

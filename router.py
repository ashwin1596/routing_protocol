from enum import Enum


class Router(Enum):
    QUEEG = 0
    COMET = 1
    RHEA = 2
    GLADOS = 3


def get_router_by_name(name):
    if name in Router.__members__:
        return Router[name]

    return None


def get_enum_from_value(value):
    for router in Router:
        if router.value == value:
            return router

    return None

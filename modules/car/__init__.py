
from .car import Car

def initialize(db_conn, shared_context):
    return Car().initialize(db_conn, shared_context)


def deinitialize():
    return Car().deinitialize()
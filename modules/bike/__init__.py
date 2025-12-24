from .bike import Bike

def initialize(db_conn, shared_context):
    return Bike().initialize(db_conn, shared_context)

def deinitialize():
    return Bike().deinitialize()
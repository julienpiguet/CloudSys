import imp
from .local_store import LocalStore
from .google_store import GoogleStore
from .exoscale_store import ExoStore

def get_store(name='local', arg = None):
    if name == 'google':
        return GoogleStore(arg) if arg != None else GoogleStore()
    if name == 'exoscale':
        return ExoStore(arg) if arg != None else ExoStore()    
    else:
        return LocalStore(arg) if arg != None else LocalStore()
    
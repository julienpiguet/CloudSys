from .local_store import LocalStore
from .google_store import GoogleStore

def get_store(name='local', arg = None):
    if name == 'google':
        return GoogleStore(arg) if arg != None else GoogleStore()
    else:
        return LocalStore(arg) if arg != None else LocalStore()
    
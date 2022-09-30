from .local_store import LocalStore

def get_store(name='default'):
    if name == 'default':
        return LocalStore('../data.json')
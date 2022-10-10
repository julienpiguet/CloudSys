import imp
from .local_store import LocalStore
from .google_store import GoogleStore
from .exoscale_store import ExoStore
from .aws_store import AWSStore
from .azure_store import AzureStore


def get_store(name='local', arg = None):
    if name == 'google':
        return GoogleStore(arg) if arg != None else GoogleStore()
    elif name == 'exoscale':
        return ExoStore(arg) if arg != None else ExoStore()  
    elif name == 'aws':
        return AWSStore(arg) if arg != None else AWSStore()
    elif name == 'azure':
        return AzureStore(arg) if arg != None else AzureStore()    
    else:
        return LocalStore(arg) if arg != None else LocalStore()
    

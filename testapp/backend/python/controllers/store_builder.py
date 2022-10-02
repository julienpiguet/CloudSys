import imp
from .local_store import LocalStore
from .google_store import GoogleStore
from .exoscale_store import ExoStore
from .aws_store import AWSStore
<<<<<<< HEAD
=======
from .azure_store import AzureStore
>>>>>>> a2aad9becf19835f4de021bdc0644be4398a8b85

def get_store(name='local', arg = None):
    if name == 'google':
        return GoogleStore(arg) if arg != None else GoogleStore()
    elif name == 'exoscale':
        return ExoStore(arg) if arg != None else ExoStore()  
    elif name == 'aws':
        return AWSStore(arg) if arg != None else AWSStore()
<<<<<<< HEAD
=======
    elif name == 'azure':
        return AzureStore(arg) if arg != None else AzureStore()    
>>>>>>> a2aad9becf19835f4de021bdc0644be4398a8b85
    else:
        return LocalStore(arg) if arg != None else LocalStore()
    

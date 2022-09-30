from .store import Store
from .item import Item
import json
import os

class LocalStore(Store):
    file: str

    def __init__(self, file='../data.json'):
        self.file = file
        if (os.path.exists(file) == False):
            f = open(file, "w+")
            f.write('{"data":[]}')
            f.close()
    
    def postItem(self, item):
        with open(self.file,'r+') as file:
            data = json.load(file)
            data['data'].append(item.__dict__)
            file.seek(0)
            json.dump(data, file)
    
    def getAllItems(self):
        f = open(self.file)
        data = json.load(f)
        return data
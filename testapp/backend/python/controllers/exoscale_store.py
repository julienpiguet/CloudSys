from fileinput import filename
from unittest import result
from .store import Store
from .item import Item
import json
import exoscale

class ExoStore(Store):
    bucket_name: str

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
    
    def postItem(self, item):
        file_name = '/tmp/'+ item.id+'.json'

        storage_client = exoscale.Exoscale()
        storage_client.storage.create_bucket(self.bucket_name, zone="ch-gva-2")
        bucket = storage_client.storage.get_bucket(self.bucket_name)
        
        f = open(file_name, "w")
        f.write(json.dumps(item.__dict__))
        f.close()
        bucket.put_file(file_name)    
    
    def getAllItems(self):
        storage_client = exoscale.Exoscale()
        bucket = storage_client.storage.get_bucket(self.bucket_name)
        list = json.loads("[]")

        for f in bucket.list_files():
            data = json.load(f.content.read())
            list.append(data)
        return list
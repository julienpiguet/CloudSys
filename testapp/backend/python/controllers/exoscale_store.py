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
        blob_name = item.id+'.json'

        storage_client = exoscale.Exoscale()
        bucket = storage_client.get_bucket(self.bucket_name)
        blob = bucket.blob(blob_name)
        with blob.open("w") as f:
            f.write(json.dumps(item.__dict__))

        bucket.put(blob, blob_name)    
    
    def getAllItems(self):
        storage_client = exoscale.Exoscale()
        bucket = storage_client.get_bucket(self.bucket_name)
        list = json.loads("[]")
        for blob in bucket.list_files():
            with blob.open("r") as f:
                data = json.load(f)
                list.append(data)
        return list
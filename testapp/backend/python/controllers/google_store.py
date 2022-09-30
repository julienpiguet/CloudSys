from .store import Store
from .item import Item
import json
from google.cloud import storage

class GoogleStore(Store):
    bucket_name: str

    def __init__(self, bucket_name):
        self.name = bucket_name
    
    def postItem(self, item):
        blob_name = item.id+'.json'

        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(blob_name)
        with blob.open("w") as f:
            f.write(json.dumps(item.__dict__))
    
    def getAllItems(self):
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        list = json.loads("[]")
        for blob in bucket.list_blobs():
            with blob.open("r") as f:
                data = json.load(f)
                list.append(data)
        return list
from fileinput import filename
from unittest import result
from .store import Store
from .item import Item
import os
import json
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__


class AzureStore(Store):
    bucket_name: str

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.conn_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    
    def postItem(self, item):

        file_name = '/tmp/'+ item.id+'.json'
        bucket_file = item.id + '.json'

        blob = BlobClient.from_connection_string(conn_str=self.conn_str, container_name=self.bucket_name, blob_name=file_name)
        
        f = open(file_name, "w")
        f.write(json.dumps(item.__dict__))
        f.close()
        with open(file_name, "rb") as data:
            blob.upload_blob(data)

    
    def getAllItems(self):
        container = ContainerClient.from_connection_string(conn_str=self.conn_str, container_name=self.bucket_name)
        list = json.loads('{ "data": []}')
        blob_list = container.list_blobs()
        for blob in blob_list:
            blobc = BlobClient.from_connection_string(conn_str=self.conn_str, container_name=self.bucket_name, blob_name=blob.name)
            blob_data = blobc.download_blob().readall()
            json_data = json.loads(blob_data)
            list['data'].append(json_data)

        return list
from fileinput import filename
from unittest import result
from .store import Store
from .item import Item
<<<<<<< HEAD
import json
from azure.storage.blob import BlobServiceClient
=======
import os
import json
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

>>>>>>> a2aad9becf19835f4de021bdc0644be4398a8b85

class AzureStore(Store):
    bucket_name: str

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.conn_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    
    def postItem(self, item):

        file_name = '/tmp/'+ item.id+'.json'
        bucket_file = item.id + '.json'

<<<<<<< HEAD
        blob_service_client = BlobServiceClient.from_connection_string(self.conn_str)
=======
        blob = BlobClient.from_connection_string(conn_str=self.conn_str, container_name=self.bucket_name, blob_name=file_name)
>>>>>>> a2aad9becf19835f4de021bdc0644be4398a8b85
        
        f = open(file_name, "w")
        f.write(json.dumps(item.__dict__))
        f.close()
<<<<<<< HEAD

        blob_client = blob_service_client.get_blob_client(container=self.bucket_name, blob=file_name)
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)
    
    def getAllItems(self):
      file_name = '/tmp/items.json'
      blob_client = blob_service_client.get_container_client(container= self.buket_name) 
      with open(download_file_path, "wb") as download_file:
      download_file.write(blob_client.download_blob(blob.name).readall())

        list = json.loads("[]")

        for f in file_name:
            data = json.load(f.content.read())
            list.append(data)
=======
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

>>>>>>> a2aad9becf19835f4de021bdc0644be4398a8b85
        return list
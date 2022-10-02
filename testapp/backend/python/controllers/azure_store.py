from fileinput import filename
from unittest import result
from .store import Store
from .item import Item
import json
from azure.storage.blob import BlobServiceClient

class AzureStore(Store):
    bucket_name: str

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.conn_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    
    def postItem(self, item):

        file_name = '/tmp/'+ item.id+'.json'
        bucket_file = item.id + '.json'

        blob_service_client = BlobServiceClient.from_connection_string(self.conn_str)
        
        f = open(file_name, "w")
        f.write(json.dumps(item.__dict__))
        f.close()

        blob_client = blob_service_client.get_blob_client(container=self.bucket_name, blob=file_name)
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)
    
    def getAllItems(self):
      file_name = '/tmp/items.json'
      blob_client = blob_service_client.get_container_client(container= self.buket_name) 
      print("\nDownloading blob to \n\t" + download_file_path)

      with open(download_file_path, "wb") as download_file:
      download_file.write(blob_client.download_blob(blob.name).readall())

        list = json.loads("[]")

        for f in file_name:
            data = json.load(f.content.read())
            list.append(data)
        return list
import json
from .item import Item
from .store import Store
import boto3

class AWSStore(Store):
    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-1',
        aws_access_key_id='XXXXXXX',
        aws_secret_access_key='XXXXXXX'
    )
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

    def postItem(self, item):
        storage_client = self.s3
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(item.name)
        blob.upload_from_string(json.dumps(item.__dict__))
        return item

    def getAllItems(self):
        storage_client = self.s3
        bucket = storage_client.bucket(self.bucket_name)
        blobs = bucket.list_blobs()
        list = {"data":[]}
        for blob in blobs:
            list["data"].append(json.loads(blob.download_as_string()))

        return list

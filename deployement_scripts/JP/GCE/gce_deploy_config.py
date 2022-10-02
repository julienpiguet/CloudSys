import googleapiclient.discovery
from google.cloud import storage
from typing import Iterable
import os
import time
from google.api_core.extended_operation import ExtendedOperation
from google.cloud import compute_v1


compute = googleapiclient.discovery.build('compute', 'v1')

project="sanguine-medley-363719"
zone="europe-west6-a"
location = 'EUROPE-WEST6'


def list_instances(project_id, zone):
    instance_client = compute_v1.InstancesClient()
    instance_list = instance_client.list(project=project_id, zone=zone)
    print(f"Instances found in zone {zone}:")
    for instance in instance_list:
        print(f" - {instance.name} ({instance.machine_type})")
        
        
def wait_for_operation(compute, project, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()
        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result
        time.sleep(1)

def create_instance(compute, project, zone, name, scriptname):
    # Get the latest Debian Jessie image.
    image_response = compute.images().getFromFamily(
        project='ubuntu-os-cloud', family='ubuntu-2204-lts').execute()
    source_disk_image = image_response['selfLink']

    # Configure the machine
    machine_type = "zones/%s/machineTypes/e2-micro" % zone
    startup_script = open(
        os.path.join(
            os.path.dirname(__file__), scriptname), 'r').read()


    config = {
        'name': name,
        'machineType': machine_type,

        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
        ],

        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],

        # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],

        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': {
            'items': [{
                # Startup script is automatically executed by the
                # instance upon startup.
                'key': 'startup-script',
                'value': startup_script
            }]
        }
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()

def create_bucket(bucket_name, project,location):
    storage_client = storage.Client(project=project)
    bucket = storage_client.bucket(bucket_name)
    bucket.create(location=location,predefined_acl='publicReadWrite')
    print(f"Bucket {bucket.name} created.")


operation = create_instance(compute, project, zone, "backend-1" ,"../../deploy_app/deploy_backend.sh")
wait_for_operation(compute, project, zone, operation['name'])

operation = create_instance(compute, project, zone, "frontend-1" ,"../../deploy_app/deploy_frontend.sh")
wait_for_operation(compute, project, zone, operation['name'])

list_instances(project, zone)
    
create_bucket("cloudsys_bucket", project,location)
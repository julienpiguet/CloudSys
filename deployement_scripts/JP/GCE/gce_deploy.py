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
bucket_name = "cloudsys-bucket-2"
frontend_name = "frontend-2"
backend_name = "backend-2"

def cmd_frontend(api):
    return '''#!/usr/bin/env bash
sudo apt update
sudo apt -y upgrade
sudo apt -y install git
cd /var
sudo mkdir www
sudo chmod 777 www/
cd www/
git clone https://github.com/julienpiguet/CloudSys.git
cd CloudSys/testapp/frontend/testapp
chmod +x deploy.sh 
sudo ./deploy.sh {api}
'''.format(api=api)

def cmd_backend(cloud,bucket):
    return '''#!/usr/bin/env bash
sudo apt update
sudo apt -y upgrade
sudo apt -y install git
cd /var
sudo mkdir www
sudo chmod 777 www/
cd www/
git clone https://github.com/julienpiguet/CloudSys.git
cd CloudSys/testapp/backend/
chmod +x deploy_python.sh 
sudo ./deploy_python.sh {cloud} {bucket}
'''.format(cloud=cloud,bucket=bucket )

# List all instances
def list_instances(project_id, zone):
    instance_client = compute_v1.InstancesClient()
    instance_list = instance_client.list(project=project_id, zone=zone)
    print(f"Instances found in zone {zone}:")
    for instance in instance_list:
        print(f" - {instance.name} ({instance.machine_type})")
        
# Wait until the new VM is created
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

# Create a new VM (instance)
def create_instance(compute, project, zone, name, scriptname):
    # Get the latest Ubuntu image.
    image_response = compute.images().getFromFamily(
        project='ubuntu-os-cloud', family='ubuntu-2204-lts').execute()
    source_disk_image = image_response['selfLink']

    # Configure the machine
    machine_type = "zones/%s/machineTypes/e2-micro" % zone
    startup_script = scriptname

    # Instance configuration
    config = {
        'name': name,
        'machineType': machine_type,
        "tags": {
            "items": ["http-server"],
        },
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
        ],
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],
        'metadata': {
            'items': [{
                'key': 'startup-script',
                'value': startup_script
            }]
        }
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()

# Create a bucket
def create_bucket(bucket_name, project,location):
    storage_client = storage.Client(project=project)
    bucket = storage_client.bucket(bucket_name)
    bucket.create(location=location,predefined_acl='publicReadWrite')
    print(f"Bucket {bucket.name} created.")
    
# Create the bucket
create_bucket(bucket_name, project,location)

# Create backend VM
print("Create instance {name}".format(name=backend_name))
operation = create_instance(compute, project, zone, backend_name , cmd_backend("google", bucket_name))
wait_for_operation(compute, project, zone, operation['name'])
backend = compute_v1.InstancesClient().get(project=project, zone=zone, instance=backend_name)
print(f" - {backend.name}, ip_interne: {backend.network_interfaces[0].network_i_p}, ip_externe: {backend.network_interfaces[0].access_configs[0].nat_i_p}, status: {backend.status}, tags: {backend.tags.items}")

# Create frontend VM
print("Create instance {name}".format(name=frontend_name))
operation = create_instance(compute, project, zone, frontend_name ,cmd_frontend(backend.network_interfaces[0].access_configs[0].nat_i_p))
wait_for_operation(compute, project, zone, operation['name'])
frontend = compute_v1.InstancesClient().get(project=project, zone=zone, instance=frontend_name)
print(f" - {frontend.name}, ip_interne: {frontend.network_interfaces[0].network_i_p}, ip_externe: {frontend.network_interfaces[0].access_configs[0].nat_i_p}, status: {frontend.status}, tags: {frontend.tags.items}")

# List all instance, must show the new VMs
list_instances(project, zone)


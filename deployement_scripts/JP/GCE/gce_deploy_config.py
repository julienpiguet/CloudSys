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
bucket_name = "cloudsys-bucket-5"
frontend_name = "frontend-5"
backend_name = "backend-5"

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
    # Get the latest Ubuntu image.
    image_response = compute.images().getFromFamily(
        project='ubuntu-os-cloud', family='ubuntu-2204-lts').execute()
    source_disk_image = image_response['selfLink']

    # Configure the machine
    machine_type = "zones/%s/machineTypes/e2-micro" % zone
    startup_script = scriptname
    #startup_script = open(
    #    os.path.join(
    #        os.path.dirname(__file__), scriptname), 'r').read()


    config = {
        'name': name,
        'machineType': machine_type,
        "tags": {
            "items": ["http-server"],
        },

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


print("Create instance {name}".format(name=backend_name))
operation = create_instance(compute, project, zone, backend_name , cmd_backend("google", bucket_name))
wait_for_operation(compute, project, zone, operation['name'])

print("Create instance {name}".format(name=frontend_name))
operation = create_instance(compute, project, zone, frontend_name ,cmd_frontend("localhost"))
wait_for_operation(compute, project, zone, operation['name'])

list_instances(project, zone)
    
create_bucket(bucket_name, project,location)
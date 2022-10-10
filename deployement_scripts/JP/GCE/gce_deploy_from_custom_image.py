import googleapiclient.discovery
from google.cloud import storage
from typing import Iterable
import re
import sys
from typing import Any, List
import warnings

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

def get_image_from_family(project: str, family: str) -> compute_v1.Image:
    image_client = compute_v1.ImagesClient()
    newest_image = image_client.get_from_family(project=project, family=family)
    return newest_image

def disk_from_image(disk_type: str,disk_size_gb: int,boot: bool,source_image: str,auto_delete: bool = True,) -> compute_v1.AttachedDisk:
    boot_disk = compute_v1.AttachedDisk()
    initialize_params = compute_v1.AttachedDiskInitializeParams()
    initialize_params.source_image = source_image
    initialize_params.disk_size_gb = disk_size_gb
    initialize_params.disk_type = disk_type
    boot_disk.initialize_params = initialize_params
    boot_disk.auto_delete = auto_delete
    boot_disk.boot = boot
    return boot_disk

def wait_for_extended_operation(operation: ExtendedOperation, verbose_name: str = "operation", timeout: int = 300) -> Any:

    result = operation.result(timeout=timeout)

    if operation.error_code:
        print(
            f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}",
            file=sys.stderr,
            flush=True,
        )
        print(f"Operation ID: {operation.name}", file=sys.stderr, flush=True)
        raise operation.exception() or RuntimeError(operation.error_message)

    if operation.warnings:
        print(f"Warnings during {verbose_name}:\n", file=sys.stderr, flush=True)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}", file=sys.stderr, flush=True)

    return result

def create_instance(
    project_id: str,
    zone: str,
    instance_name: str,
    disks: List[compute_v1.AttachedDisk],
    machine_type: str = "n1-standard-1",
    network_link: str = "global/networks/default",
    subnetwork_link: str = None,
    internal_ip: str = None,
    external_access: bool = False,
    external_ipv4: str = None,
    accelerators: List[compute_v1.AcceleratorConfig] = None,
    preemptible: bool = False,
    spot: bool = False,
    instance_termination_action: str = "STOP",
    custom_hostname: str = None,
    delete_protection: bool = False,
) -> compute_v1.Instance:

    instance_client = compute_v1.InstancesClient()

    # Use the network interface provided in the network_link argument.
    network_interface = compute_v1.NetworkInterface()
    network_interface.name = network_link
    if subnetwork_link:
        network_interface.subnetwork = subnetwork_link

    if internal_ip:
        network_interface.network_i_p = internal_ip

    if external_access:
        access = compute_v1.AccessConfig()
        access.type_ = compute_v1.AccessConfig.Type.ONE_TO_ONE_NAT.name
        access.name = "External NAT"
        access.network_tier = access.NetworkTier.PREMIUM.name
        if external_ipv4:
            access.nat_i_p = external_ipv4
        network_interface.access_configs = [access]

    # Collect information into the Instance object.
    instance = compute_v1.Instance()
    instance.network_interfaces = [network_interface]
    instance.name = instance_name
    instance.disks = disks
    if re.match(r"^zones/[a-z\d\-]+/machineTypes/[a-z\d\-]+$", machine_type):
        instance.machine_type = machine_type
    else:
        instance.machine_type = f"zones/{zone}/machineTypes/{machine_type}"

    if accelerators:
        instance.guest_accelerators = accelerators

    if preemptible:
        # Set the preemptible setting
        warnings.warn(
            "Preemptible VMs are being replaced by Spot VMs.", DeprecationWarning
        )
        instance.scheduling = compute_v1.Scheduling()
        instance.scheduling.preemptible = True

    if spot:
        # Set the Spot VM setting
        instance.scheduling = compute_v1.Scheduling()
        instance.scheduling.provisioning_model = (
            compute_v1.Scheduling.ProvisioningModel.SPOT.name
        )
        instance.scheduling.instance_termination_action = instance_termination_action

    if custom_hostname is not None:
        # Set the custom hostname for the instance
        instance.hostname = custom_hostname

    if delete_protection:
        # Set the delete protection bit
        instance.deletion_protection = True
    
    instance.tags = compute_v1.Tags().items.append('http-server')

    # Prepare the request to insert an instance.
    request = compute_v1.InsertInstanceRequest()
    request.zone = zone
    request.project = project_id
    request.instance_resource = instance

    # Wait for the create operation to complete.
    print(f"Creating the {instance_name} instance in {zone}...")

    operation = instance_client.insert(request=request)

    wait_for_extended_operation(operation, "instance creation")

    print(f"Instance {instance_name} created.")
    return instance_client.get(project=project_id, zone=zone, instance=instance_name)

def create_from_custom_image(
    project_id: str, zone: str, instance_name: str, custom_image_link: str
) -> compute_v1.Instance:

    disk_type = f"zones/{zone}/diskTypes/pd-standard"
    disks = [disk_from_image(disk_type, 10, True, custom_image_link, True)]
    instance = create_instance(project_id, zone, instance_name, disks, machine_type="e2-micro", external_access=True)
    
    return instance


    
def create_bucket(bucket_name, project,location):
    storage_client = storage.Client(project=project)
    bucket = storage_client.bucket(bucket_name)
    bucket.create(location=location,predefined_acl='publicReadWrite')
    print(f"Bucket {bucket.name} created.")
    
    
create_from_custom_image(project, zone, "frontend-2", "projects/"+project+"/global/images/cloudsys-frontend")
create_from_custom_image(project, zone, "backend-1", "projects/"+project+"/global/images/cloudsys-backend")
    
list_instances(project, zone)
    
create_bucket("cloudsys_bucket", project,location)
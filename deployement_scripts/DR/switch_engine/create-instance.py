import openstack
import openstack.config.loader
import openstack.compute.v2.server
import os
import argparse
import errno

# Initialize and turn on debug logging

# Initialize connection

# List the servers

backendScript =  '''#!/usr/bin/env bash
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
sudo ./deploy_python.sh amazon cloud-bucket
'''

frontendScript =  '''#!/usr/bin/env bash
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
sudo ./deploy.sh google
'''

def create_connection_from_config():
    return openstack.connect(cloud='engines')

def create_connection_from_args():
    parser = argparse.ArgumentParser()
    return openstack.connect(options=parser)

def create_keypair(conn):
    keypair = conn.compute.find_keypair("switch_engine_key")

    if not keypair:
        print("Create Key Pair:")

        keypair = conn.compute.create_keypair(name="switch_engine_key")

        print(keypair)

        try:
            os.mkdir("/home/denis/.ssh")
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e

        with open("switch_engine_key", 'w') as f:
            f.write("%s" % keypair.private_key)

        os.chmod("switch_engine_key", 0o400)

    return keypair

def create_server(conn, end="backend"):
    print("Create Server:")
    image = conn.compute.find_image("Ubuntu Jammy 22.04 (SWITCHengines)")
    flavor = conn.compute.find_flavor("m1.small")
    network = conn.network.find_network("private")
    keypair = create_keypair(conn)
    server = conn.compute.create_server(
        name="cloudsys-lab1-backend", image_id=image.id, flavor_id=flavor.id,
        networks=[{"uuid": network.id}], key_name=keypair.name)
    server = conn.compute.wait_for_server(server)
    create_keypair(conn)
    # find avaiable floating ip
    floating_ip = conn.network.find_available_ip()
    conn.compute.add_floating_ip_to_server(server, floating_ip.floating_ip_address)
    # add instance to all security groups
    for sg in conn.network.security_groups():
        conn.network.add_interface_to_security_group(sg, server_id=server.id)
    print("ssh -i {key} root@{ip}".format(
        key="switch_engine_key",
        ip=floating_ip.floating_ip_address))
    #print floatin ip
    # execute bash script on server
    if end=="backend":
        conn.compute.run_server_script(server, backendScript)
    elif end=="frontend":
        conn.compute.run_server_script(server, frontendScript)

def list_servers(conn):
    print("List Servers:")

    for server in conn.compute.servers():
        print(server)


conn = create_connection_from_config()
create_server(conn, "backend")
create_server(conn, "frontend")
list_servers(conn)

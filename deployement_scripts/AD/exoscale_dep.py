import exoscale
exo = exoscale.Exoscale()

zname="ch-gva-2"
zone = exo.compute.get_zone(zname)
type = exo.compute.get_instance_type("tiny")
security_group = exo.compute.get_security_group(name='cloudsys')
bucket_name = 'cloudsys-bucket-2'

def cmd_frontend(api):
    return '''#cloud-config
runcmd:
 - sudo apt update
 - sudo apt -y upgrade
 - sudo apt -y install git
 - cd /var
 - sudo mkdir www
 - sudo chmod 777 www/
 - cd www/
 - git clone https://github.com/julienpiguet/CloudSys.git
 - cd CloudSys/testapp/frontend/testapp
 - chmod +x deploy.sh 
 - sudo ./deploy.sh {api}
'''.format(api=api)

def cmd_backend(cloud,bucket):
    return '''#cloud-config
runcmd:
 - sudo apt update
 - sudo apt -y upgrade
 - sudo apt -y install git
 - cd /var
 - sudo mkdir www
 - sudo chmod 777 www/
 - cd www/
 - git clone https://github.com/julienpiguet/CloudSys.git
 - cd CloudSys/testapp/backend/
 - chmod +x deploy_python.sh 
 - sudo ./deploy_python.sh {cloud} {bucket}
'''.format(cloud=cloud,bucket=bucket )


def create_instance(exo, name, zone, type, security_group, cmd):
    print('Creating {name}'.format(name=name))
    instance = exo.compute.create_instance( 
        name=name, 
        zone=zone, 
        type=type, 
        template=list(
            exo.compute.list_instance_templates(
                zone,
                "Linux Ubuntu 22.04 LTS 64-bit"))[0],
        volume_size=10, 
        security_groups=[security_group],
        user_data=cmd
    )
    return instance

security_group_web = exo.compute.get_security_group(name='web')

if not security_group_web:
    security_group_web = exo.compute.create_security_group("web")

    for rule in [
        exoscale.api.compute.SecurityGroupRule.ingress(
            description="HTTP",
            network_cidr="0.0.0.0/0",
            port="80",
            protocol="tcp",
        ),
        exoscale.api.compute.SecurityGroupRule.ingress(
            description="HTTPS",
            network_cidr="0.0.0.0/0",
            port="443",
            protocol="tcp",
        ),
    ]:
        
        security_group_web.add_rule(rule)
    

backend = create_instance(exo, 'backend-2', zone, type, security_group_web, cmd_backend('exoscale', bucket_name))
print('Backend avalable at {ip}'.format(ip=backend.ipv4_address))

frontend = create_instance(exo, 'frontend-2', zone, type, security_group_web, cmd_frontend(backend.ipv4_address))
print('Frontend avalable at {ip}'.format(ip=frontend.ipv4_address))


bucket = exo.storage.create_bucket(name=bucket_name, zone=zname)
print('Bucket {name} as been created'.format(name=bucket.name)) 
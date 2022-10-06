import paramiko
import time 
import webbrowser
import boto3


FRONT_END_IMAGE = 'ami-03d04cb5178d0637d'
BACK_END_IMAGE = 'ami-03d04cb5178d0637d'


def RetrievePublicIP(frontID, backID):
    frontIP = ""
    backIP = ""
    client = boto3.client('ec2')
    instance_dict = client.describe_instances().get('Reservations')
    for reservation in instance_dict:
        for instance in reservation['Instances']: # This is rather not obvious
            if instance['State']['Name'] == 'running' and instance['PublicIpAddress'] != None:
                if instance['InstanceId'] == frontID:
                    frontIP = instance['PublicIpAddress']
                elif instance['InstanceId'] == backID:
                    backIP = instance['PublicIpAddress']
    return frontIP, backIP



#Create instances 

ec2 = boto3.resource('ec2')


#create front instance
frontInstance = ec2.create_instances(
        ImageId= FRONT_END_IMAGE,
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="KeyPairGroupe3_BG"
    )

backInstance = ec2.create_instances(
        ImageId= BACK_END_IMAGE,
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="KeyPairGroupe3_BG"
    )

# Retrieve ip for front and backend
frontEndInstanceID = frontInstance[0].instance_id
backEndInstanceID = backInstance[0].instance_id

frontInstance[0].wait_until_running()
backInstance[0].wait_until_running()

# Wait for the instance to run 

FRONTEND_HOSTNAME, BACKEND_HOSTNAME = RetrievePublicIP(frontEndInstanceID,backEndInstanceID)

# access instance using SSH
PRIVATE_KEY_FOR_AUTH = "C:/Users/Bastien GABRIEL/Documents/00_Etudes/05_HESSO_Master/00_Hiver/00_CloudSystem/02_Labo/00_Lab_1/AWS/Keys/KeyPairGroupe3_BG.pem"
FRONTEND_PORT = "8080"
CONFIG_FILE_PATH = "/home/ec2-user/source/CloudSys/testapp/frontend/testapp/src/config.js"
FRONT_END_DIR = "/home/ec2-user/source/CloudSys/testapp/frontend/testapp"
SSH_USER = "ec2-user"


#Connect to backend instance

#Run backend 
#print("LOG: Accessing backend instance through SSH")
#ssh_client_back = paramiko.SSHClient()
#ssh_client_back.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#ssh_client_back.connect(hostname=BACKEND_HOSTNAME, username=SSH_USER, port=22,key_filename=PRIVATE_KEY_FOR_AUTH)
#
#ssh_client_back.close()

#Connect to frontend instance
print("LOG: Accessing frontend instance through SSH")
ssh_client_front = paramiko.SSHClient()
ssh_client_front.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client_front.connect(hostname=FRONTEND_HOSTNAME, username=SSH_USER, port=22,key_filename=PRIVATE_KEY_FOR_AUTH)

#Edit config.js file to change the ip address of the 
# backend in the config file  
print("LOG: Edit config.js on frontend instance at " + FRONTEND_HOSTNAME)
configFileContent = """
module.exports = {
    API_LOCATION: "'"http://localhost:3000\"'"
  } """
newConfigFileContent = configFileContent.replace("localhost", BACKEND_HOSTNAME)

command = " echo \"" + newConfigFileContent + "\" > " + CONFIG_FILE_PATH
print("Executing command : " + command)
stdin,stdout,stderr=ssh_client_front.exec_command(command)
print(stdout.readlines())

# Run frontend
print("LOG: Running frontend")
runFrontCommand = "cd " + FRONT_END_DIR + " &&  npm run serve &"
print("Executing command : " + runFrontCommand)
stdin,stdout,stderr=ssh_client_front.exec_command(runFrontCommand)

#Open browser after 5 seconds
time.sleep(5)


#Open webbrower
frontendWebURL = "http://"+FRONTEND_HOSTNAME+ ":" + FRONTEND_PORT + "/"
print("LOG: Opening website at " + frontendWebURL)
webbrowser.open(frontendWebURL , new=2)



s = input()

import json
import boto3
import sys
import os

# Get list of any chargable active resources (EC2, RDS, volumes/snapshots, EIPs etc)
# Check if they have an exclusion tag
# Report both categories to SNS topic
# Have switch function to allow stopping or even deleting stray resources
# I test this on a box with python 3.7.10 so I guess run with that version

# Can't seem to get global variables etc to work, makes for a messy way of setting the region
# Also this isn't about the python, it's about the lambda... 

def check_AMI():
    image_list=""
    AWS_region=os.environ['AWS_REGION']
    AMI=boto3.client('ec2', region_name=AWS_region )
    all_images=AMI.describe_images(Owners=['self'])
    for images in all_images['Images']:
        image_list=image_list + images['ImageId'] + "\t" + images['CreationDate'] + '\n ' 
    return image_list


def check_snaps():
    snapshot_list=""
    AWS_region=os.environ['AWS_REGION']
    SNAPS=boto3.client('ec2', region_name=AWS_region )
    all_snaps=SNAPS.describe_snapshots(OwnerIds=['self'])
    for snapshot in all_snaps['Snapshots']:
        snapshot_list=snapshot_list + snapshot['SnapshotId'] + "\t" + str(snapshot['StartTime']) + '\n ' 
    return snapshot_list


def check_RDS():
    instance_list=""
    AWS_region=os.environ['AWS_REGION']
    RDS=boto3.client('rds', region_name=AWS_region )

    all_instances=RDS.describe_db_instances()
    for instance in all_instances['DBInstances']:
        instance_list=instance_list  + instance['DBInstanceIdentifier'] + "\t"  + instance['DBInstanceStatus'] + '\n '
    return instance_list



def check_EC2():
    instance_list=""
    AWS_region=os.environ['AWS_REGION']
    EC2=boto3.resource('ec2', region_name=AWS_region)
    all_instances=EC2.instances.all()

    for instance in all_instances:
    #    print(f'Tags: {instance.tags.value}')
        instance_list=instance_list  +instance.id + "\t" + instance.state["Name"] + '\n '
    return instance_list 


def send_SNS(subject,message):
    sns = boto3.client('sns')
    sns_arn=os.environ['MY_SNS_TOPIC_ARN']
    response = sns.publish(
        TopicArn=sns_arn,
        Message=message,
        Subject=subject,
    )


def lambda_handler(event, context):
    EC2_list=""
    RDS_list=""
    AMI_list=""
    snap_list=""
    action=event['Action']
    if (action =="List"):
        EC2_list=check_EC2()
        RDS_list=check_RDS()
        AMI_list=check_AMI()
        print ("AMI LIST: \n" + AMI_list)
        SNAP_list=check_snaps()
        send_SNS("Running Resources:","EC2s:\n" + EC2_list + "\nRDS Instances:\n" + RDS_list + "\nAMIs\n" + AMI_list+ "\nSnapshots:\n" + SNAP_list)
    elif (action == "Debug"):
        ret_str=("PARAMETERS:\n" + json.dumps(event) + "\nMY_SNS_TOPIC_ARN: ")
        ret_str=(ret_str + "VARIABLES:\n" + os.environ['MY_SNS_TOPIC_ARN'] + "\n" + os.environ['AWS_REGION'])
        send_SNS("Debug info", ret_str)
    else:
        send_SNS("ERROR", json.dumps(event))


    return {
        'statusCode': 200,
        'body': json.dumps(EC2_list + "\n" + RDS_list)
    }


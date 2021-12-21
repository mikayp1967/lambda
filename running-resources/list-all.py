import json
import boto3
import sys
import os

# Get list of any chargable active resources (EC2, RDS, volumes/snapshots, EIPs etc)
# Check if they have an exclusion tag
# Report both categories to SNS topic
# Have switch function to allow stopping or even deleting stray resources
# I test this on a box with python 3.7.10 so I guess run with that version



def check_RDS():
    instance_list=""
    RDS=boto3.client('rds' )
    all_instances=RDS.describe_db_instances()
    for instance in all_instances['DBInstances']:
        print(f"RDS instance {instance['DBInstanceIdentifier']}  \t State: {instance['DBInstanceStatus']}")
        instance_list=instance_list + '\n ' + instance['DBInstanceIdentifier'] + "\t" + instance['DBInstanceStatus']
    return instance_list



def check_EC2():
    instance_list=""
    EC2=boto3.resource('ec2', region_name="eu-west-2")
    all_instances=EC2.instances.all()

    for instance in all_instances:
        print(f'EC2 instance {instance.id}  \t State: {instance.state["Name"]}')
    #    print(f'Tags: {instance.tags.value}')
        instance_list=instance_list + '\n ' +instance.id + "\t" + instance.state["Name"]
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
    action=event['Action']
    if (action =="List"):
        EC2_list=check_EC2()
        RDS_list=check_RDS()
        send_SNS("Running Instances", EC2_list + "\n" + RDS_list)
    elif (action == "Debug"):
        ret_str=(json.dumps(event) + "\nMY_SNS_TOPIC_ARN: " + os.environ['MY_SNS_TOPIC_ARN'])
        send_SNS("Debug info", ret_str)
    else:
        send_SNS("ERROR", json.dumps(event))


    return {
        'statusCode': 200,
        'body': json.dumps(EC2_list + "\n" + RDS_list)
    }


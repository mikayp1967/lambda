import json
import boto3
import sys
import os

# Get list of any chargable active resources (EC2, RDS, volumes/snapshots, EIPs etc)
# Check if they have an exclusion tag
# Report both categories to SNS topic
# Have switch function to allow stopping or even deleting stray resources
# I test this on a box with python 3.7.10 so I guess run with that version

sns = boto3.client('sns')
sns_arn=os.environ['MY_SNS_TOPIC_ARN']
instance_list=""



def check_EC2():
# List of EC2s
    EC2=boto3.resource('ec2', region_name="eu-west-2")
    all_instances=EC2.instances.all()

    for instance in all_instances:
        print(f'EC2 instance {instance.id}  \t State: {instance.state["Name"]}')
    #    print(f'Tags: {instance.tags.value}')
        instance_list=instance_list + '\n ' +instance.id + "\t" + instance.state["Name"]

def send_SNS(subject,message):
    response = sns.publish(
        TopicArn=sns_arn,
        Message=message,
        Subject=subject,
    )


def lambda_handler(event, context):
    action=event['Action']
    if (action =="List"):
        check_EC2()
        send_SNS("Running Instances", instance_list)
    elif (action == "Debug"):
        ret_str=(json.dumps(event) + "\nsns_arn: " + sns_arn)
        send_SNS("Debug info", ret_str)
    else:
        send_SNS("ERROR", json.dumps(event))


    return {
        'statusCode': 200,
        'body': json.dumps(instance_list)

    }


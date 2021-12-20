import json
import boto3
import sys

# Get list of any chargable active resources (EC2, RDS, volumes/snapshots, EIPs etc)
# Check if they have an exclusion tag
# Report both categories to SNS topic
# Have switch function to allow stopping or even deleting stray resources
# I test this on a box with python 3.7.10 so I guess run with that version

sns = boto3.client('sns')
topicarn="arn:aws:sns:eu-west-2::running-resources"


# List of EC2s
instance_list=""
EC2=boto3.resource('ec2', region_name="eu-west-2")
all_instances=EC2.instances.all()

for instance in all_instances:
    print(f'EC2 instance {instance.id}  \t State: {instance.state["Name"]}')
#    print(f'Tags: {instance.tags.value}')
    instance_list=instance_list + '\n ' +instance.id + "\t" + instance.state["Name"]


"""
response = sns.publish(
    TopicArn=topicarn,
    Message=instance_list,
    Subject='Running resources',
)

"""

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(instance_list)

    }


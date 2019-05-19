import json
import boto3
import sys
import datetime
from datetime import date, timedelta, datetime



sns = boto3.client('sns')
ec2 = boto3.client('ec2')


topicarn="arn:aws:sns:eu-west-2:845667357603:testtopic1"
snapshots = ec2.describe_snapshots(OwnerIds=['self'])
snapmsg="Snapshot ID: %s \tDate: %s\n"
retentionDate = datetime.now() - timedelta(days=180)
retentionDate=retentionDate.date()
snsmessage =""


print('\n\nDeleting all Snapshots older than %s\n\n' % retentionDate)

for i in snapshots['Snapshots']:
    if i['StartTime'].date() < retentionDate:
        snsmessage=snsmessage+snapmsg%(i['SnapshotId'],i['StartTime'].date())
        

if snsmessage:
    retmsg="List of snapshots older than " + str(retentionDate) + "\n\n"+snsmessage
else:
    retmsg="There are no old snapshots\n"


response = sns.publish(
    TopicArn=topicarn,
    Message=retmsg,
    Subject='Lambda abdcef old snapshot list',
)




def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(retmsg)

    }


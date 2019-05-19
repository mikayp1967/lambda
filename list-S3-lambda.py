import json
import boto3
import sys


s3=boto3.client('s3')
all_buckets=s3.list_buckets()
bucketlist=""
for bucket in all_buckets['Buckets']:
    print (bucket['Name'])
    bucketlist=bucketlist + '\n ' +bucket['Name']

retmsg='List of buckets:' + bucketlist


sns = boto3.client('sns')
topicarn="arn:aws:sns:eu-west-2:845667357603:testtopic1"

response = sns.publish(
    TopicArn=topicarn,
    Message=retmsg,
    Subject='Lambda abdcef bucket list',
)



def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(retmsg)

    }



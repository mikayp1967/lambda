# Running Resources

* Create lambda that list any chargable active resources  and potentially stops/deletes them
* Create SNS topic to send a report to
* Build it all with cloudformation
* Have a codebuild pipeline to create/destroy it all


## Completed

* Create basic Lambda function and permissions required to run
* Create SNS
  * Reference SNS
* Create Eventbridge Event to trigger the lambda
* Basic scanning of RDS resources
* Extend lambda code
  *  Find other resources (RDS, Snapshots, AMIs)       


## To do
  
* Codebuild pipeline to deploy it all
* Extend lambda code
  *  Find other resources (EIP, NGW, Unattached Volumes) - bored of this for now, not really the point anyway
  *  Filter out resources that have certain tags
  *  Allow invocation to stop resources (where applicable)
  *  Enable invocation to delete resources (where applicable)

  

## Instructions

You will need various permissions (trimmed version of following):

* AmazonS3FullAccess
* AWSLambda_FullAccess
* AmazonAPIGatewayAdministrator
* AWSCloudFormationFullAccess
* IAMFullAccess

These will change. For now this is how you deploy the lambda:

    export BUCKET=<aws bucket>
    git clone git@github.com:mikayp1967/lambda.git
    cd running-resources
    sam build                   # Do I need to do this?
    aws cloudformation package --template-file template.yaml --s3-bucket $BUCKET \ 
        --output-template-file outputtemplate.yml
    aws cloudformation deploy --template-file outputtemplate.yml \
        --capabilities CAPABILITY_IAM --stack-name running-res


## References

IAM STUFF
    https://aws.amazon.com/premiumsupport/knowledge-center/lambda-sam-template-permissions/

SNS STUFF
    https://medium.com/build-succeeded/aws-lambda-with-sam-template-to-subscribe-an-sqs-to-an-sns-topic-52102b6e4bae

CW EVENT:
    https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-schedule.html
    https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html
    https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule-schedule.html


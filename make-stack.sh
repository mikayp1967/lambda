#!/bin/bash
#
# Check if cloudformation stack (passed in $1) exists and do an update-stack
# otherwise do a create-stack

STACK_NAME=$1
STACK_TEMPLATE=$2
EXTRA_OPTS=$3


stacklines=$( aws cloudformation describe-stacks --stack-name ${STACK_NAME} 2>/dev/null|wc -l)

printf "\n\n"
 if [ ${stacklines} -gt 0 ]; then 
    printf "Already exists - updating stack\n"
    aws cloudformation update-stack --template-body file://./${STACK_TEMPLATE} --stack-name ${STACK_NAME} ${EXTRA_OPTS}
    # Wait til stack has finished building
    sleep 5         # This may stop abnormal exiting of the code?
    
    STACK_STATUS=`aws cloudformation describe-stacks --stack-name ${STACK_NAME}|grep "StackStatus"|sed 's/^.*:..//;s/\".*$//'|tail -1`
    printf "Stack status ${STACK_STATUS}\n"
    if [ ${STACK_STATUS} != "CREATE_COMPLETE" ]; then
        printf "Waiting for stack to complete...\n"
        aws cloudformation wait stack-update-complete --stack-name ${STACK_NAME} 
    else
        printf "Stack has no changes...\n"
        fi

else
    printf "DOESN'T EXIST - creating new stack\n"
    aws cloudformation create-stack --template-body file://./${STACK_TEMPLATE} --stack-name ${STACK_NAME} ${EXTRA_OPTS}
    printf "Waiting for stack to complete...\n"
    aws cloudformation wait stack-create-complete --stack-name ${STACK_NAME}      
    fi
printf "\n\n"
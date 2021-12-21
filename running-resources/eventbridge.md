The following nested under "Events:" will create a trigger for the lambda, but it doesn't seem to allow passing anything to the API
So not really possible to select whether to list resources or stop them


        RRSchedule:
          Type: Schedule
          Properties:
            Schedule: 'cron(0 * * * ? *)'
            Description: 'Schedule Resource shutdown/check'
            Enabled: true
            Name: 'Running_Resources'

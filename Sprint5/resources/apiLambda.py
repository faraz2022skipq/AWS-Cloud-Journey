from urllib import response
import boto3
import os

# Declaring constants
NAMESPACE = "Sprint5D1"
METRIC_NAME = "ARG_limit"

def lambda_handler(myEvent, context):

    # Create cloud watch client for real time alarm generation
    createAlarmclient = boto3.client("cloudwatch")
    
    # Accessing the snsARN environment variable
    snsARN = os.environ["snsARN"]

    # Getting the value
    body = myEvent["body"]
    value = int(body[8:11])

    dimensions = [{'Name': 'arg1', 'Value': str(value)}]

    matric_data = createAlarmclient.put_metric_data(Namespace = NAMESPACE,
                                    MetricData = [
                                            {
                                                'MetricName': METRIC_NAME,
                                                'Dimensions': dimensions,
                                                'Value': value,
                                            },
                                        ]
                                    )
    
    # Putting alarm on cloud watch
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_metric_alarm
    createAlarmclient.put_metric_alarm(
            AlarmName = "FarazD1",
            ComparisonOperator = "GreaterThanThreshold",
            EvaluationPeriods = 1,
            MetricName = METRIC_NAME,
            Namespace = NAMESPACE,
            Period = 60,
            Statistic = 'Average',
            Threshold = 10,
            Dimensions = dimensions,
            ActionsEnabled = True,
            AlarmActions = [snsARN]
        )

    # Generating response for API Gateway
    if myEvent["httpMethod"] == "PUT":
        response = {
            "statusCode" : 200,
            "body" : myEvent["body"],
        }

        return response
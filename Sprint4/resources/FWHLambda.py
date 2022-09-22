import datetime
import http
import urllib3
import constants as constant
from CloudWatch_Matrics import FWHCloudWatchMatric
import boto3
import os


# Creating my boto3 client for fetching data from DB
getDataclient = boto3.client("dynamodb")
# Accessing the table using environment variable
urlTable = os.environ["urlTable"]

snsARN = os.environ["snsARN"]

# Create cloud watch client for real time alarm generation
createAlarmclient = boto3.client("cloudwatch")
    
def lambda_handler(myEvent, context):
    
    # Getting data from the urlTable
    names = getData()
    print(names)
    
    # Creating dictionary for latency and availability values
    values = dict()

    for urls in names:
        print(urls)
        
        # Getting and updating the values of availability and latency
        availability = checkAvailability(urls)
        latency = getLatency(urls)
        values.update({"availability": availability, "latency": latency})

        # creating object of cloud watch matric
        FWHCW = FWHCloudWatchMatric()

        dimensions = [{'Name': 'url', 'Value': urls}]

        # Putting the availabilty matric and latency matric on cloud
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_metric_data
        response_availibility = FWHCW.put_matric_data(constant.URL_TO_MONITOR_NAMESPACE,
                                        constant.URL_TO_MONITOR_AVAILABILITY,
                                        dimensions,
                                        availability)
        response_latency = FWHCW.put_matric_data(constant.URL_TO_MONITOR_NAMESPACE,
                                        constant.URL_TO_MONITOR_LATENCY,
                                        dimensions,
                                        latency)
    
        createAlarmclient.put_metric_alarm(
            AlarmName = "FarazURLavailability-" + str(urls),
            ComparisonOperator = "LessThanThreshold",
            EvaluationPeriods = 1,
            MetricName = constant.URL_TO_MONITOR_AVAILABILITY,
            Namespace = constant.URL_TO_MONITOR_NAMESPACE,
            Period = 60,
            Statistic = 'Average',
            Threshold = 1,
            Dimensions = [{'Name': 'url', 'Value': urls}],
            ActionsEnabled = True,
            AlarmActions = [snsARN]
        )
        
        createAlarmclient.put_metric_alarm(
            AlarmName = "FarazURLlatency-" + str(urls),
            ComparisonOperator = "GreaterThanThreshold",
            EvaluationPeriods = 1,
            MetricName = constant.URL_TO_MONITOR_LATENCY,
            Namespace = constant.URL_TO_MONITOR_NAMESPACE,
            Period = 60,
            Statistic = 'Average',
            Threshold = 0.09,
            Dimensions = [{'Name': 'url', 'Value': urls}],
            ActionsEnabled = True,
            AlarmActions = [snsARN]
        )
    return values

# Checks the availibilty of the URL
def checkAvailability(to_Monitor):
    http = urllib3.PoolManager()
    availabilityResponse = http.request('GET', to_Monitor)
    if availabilityResponse.status == 200:
        return 1.0
    else:
        return 0.0

# Checks the latency of the URL
def getLatency(to_Monitor):
    http = urllib3.PoolManager()
    start = datetime.datetime.now()
    latencyResponse = http.request('GET', to_Monitor)
    end = datetime.datetime.now()
    deltaTime = end - start
    latency = round(deltaTime.microseconds * 0.000001, 6)
    return latency
    
def getData():
    # Entering the data into my DynamoDB table
    data = getDataclient.scan(TableName = urlTable, AttributesToGet=["BODY"])
    
    links = data["Items"]
    # Converting list to dictionary
    URL_names = {}
    for i in range(len(links)):
        URL_names[i] = links[i]
    # Parsing out the URL names
    names = []
    for i in range(len(URL_names)):
        names.append(URL_names[i]["BODY"]["S"])
    return names
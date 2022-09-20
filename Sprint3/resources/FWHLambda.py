import datetime
import http
import urllib3
import constants as constant
from CloudWatch_Matrics import FWHCloudWatchMatric


def lambda_handler(myEvent, context):
    values = dict()

    for urls in constant.URL_TO_MONITOR:
        
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
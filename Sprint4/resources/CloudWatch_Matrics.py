import boto3

class FWHCloudWatchMatric:

    """
    Class for using the 'put_matric_data' method of boto3 to put data on matric
    """
    def __init__(self) -> None:
        # Creating object client of boto3 CloudWatch service
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_metric_data
        self.client = boto3.client('cloudwatch')

    def put_matric_data(self, namespace, metricname, dimensions, value):
        '''
            This will put our data on the cloud watch
        '''
        response = self.client.put_metric_data(
                    Namespace = namespace,
                    MetricData = [
                        {
                            'MetricName': metricname,
                            'Dimensions': dimensions,
                            'Value': value,
                        },
                    ]
                )
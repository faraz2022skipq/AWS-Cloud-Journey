import boto3
import os
import json


def lambda_handler(myEvent, context):

    # Declaring the boto3 client for dynamodb
    DBclient = boto3.client("dynamodb")

    # Accessing the table using environment variable
    DB_Table = os.environ["AlarmTable"]
    
    # Parsing through the Json file 
    messageID = myEvent["Records"][0]["Sns"]["MessageId"]
    message = myEvent["Records"][0]["Sns"]["Message"]
    timestamp = myEvent["Records"][0]["Sns"]["Timestamp"]
    
    # Entering the data into my DynamoDB table
    DBclient.put_item(TableName = DB_Table,
        Item = {
            "ID" : {"S" : messageID},
            "Message" : {"S" : message},
            "TimeStamp" : {"S" : timestamp}
        }
    )
    return DB_Table
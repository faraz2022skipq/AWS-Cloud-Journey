from urllib import response
import boto3
import os


def lambda_handler(myEvent, context):

    # Declaring the boto3 client for dynamodb
    apiDBclient = boto3.client("dynamodb")

    # Accessing the table using environment variable
    urlTable = os.environ["urlTable"]

    body = myEvent["body"]

    if myEvent["httpMethod"] == "PUT":
        # Entering the data into my DynamoDB table
        apiDBclient.put_item(TableName = urlTable,
            Item = {
                "BODY" : {"S" : body}
            }
        )
        
        response = {
            "statusCode" : 200,
            "body" : myEvent["body"],
        }
    
    if myEvent["httpMethod"] == "GET":
        # Entering the data into my DynamoDB table
        data = apiDBclient.scan(TableName = urlTable, AttributesToGet=["BODY"])
        
        links = data["Items"]
        # Converting list to dictionary
        URL_names = {}
        for i in range(len(links)):
            URL_names[i] = links[i]
        # Parsing out the URL names
        names = []
        for i in range(len(URL_names)):
            names.append(URL_names[i]["BODY"]["S"])
        
        print(names)
        
        names = " ".join(names)
        
        response = {
            "statusCode" : 200,
            "body" : names,
        }

    if myEvent["httpMethod"] == "DELETE":
        # Entering the data into my DynamoDB table
        apiDBclient.delete_item(TableName = urlTable,
            Key = {
                "BODY" : {"S" : body}
            }
        )
        
        response = {
            "statusCode" : 200,
            "body" : myEvent["body"],
        }
    
    if myEvent["httpMethod"] == "POST":
        # Entering the data into my DynamoDB table
        toDelete, toAdd = body.split(",")
        apiDBclient.delete_item(TableName = urlTable,
            Key = {
                "BODY" : {"S" : toDelete}
            }
        )
        apiDBclient.put_item(TableName = urlTable,
            Item = {
                "BODY" : {"S" : toAdd}
            }
        )
    
        response = {
            "statusCode" : 200,
            "body" : myEvent["body"],
        }
    
    return response
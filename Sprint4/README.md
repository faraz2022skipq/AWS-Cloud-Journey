# CRUD operations using AWS Gateway REST API

The aim of this project is to create a REST API using AWS API Gateway to allow users to communicate with the application.

In this, the user can perform CRUD (Create, Read, Upgrate and Delete) operation for adding, reading, upgrading or deleting the URLs from dynamodb URL table that act as an input for our web health crawler application. We can add any number of URLs.

The web crawler will take these inputs and will create alarms, send notification to DevOps engineer if an alrams goes on and will save the alarm along with the timestamp in dynamodb Alarm tables. 

# Technologies
Project is created with following language and libraries.

* Python 3.6
* AWS CDK 2.22.0
* urllib3 1.25.8

# Sprint 4 includes following tasks:
* Create a DynamoDB table and integrate the table with the Lambda function.
* Create a REST API using AWS API Gateway and integrate it with Lambda function.
* Make Create, Read, Update and Delete (CRUD) methods and create functionalities for each method in the Lambda function.
* Read the values from DynamoDB table and create real time alarms.
* Notify the DevOps engineer regarding the Alarms via SNS topic.

# Launch
To launch this project first you need to clone the repository into your local system. You can do this by following command

``` git clone https://github.com/faraz2022skipq/Pegasus_Python.git ```

Then you have to go to the folder by following command

``` cd Pegasus_Python/faraz2022skipq/Sprint4 ```

Then you will run the following commands to install the dependencies

``` pip install -r requirements.txt ```

Now, you can work on this project in your local repository


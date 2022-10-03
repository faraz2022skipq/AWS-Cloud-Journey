# Sprint 2: First Crawl of the Spider
This project is to check the web health of a given website. We health includes the latency and availability of the website. The beauty of this project is the notification system, in which you can send an email or sms to the concerned person. 
Another feature is that it store both the latency and availability alarm data in a database so we can have data to work upon in future.

# AWS Services Used
1. AWS IAM
2. AWS Lambda
3. AWS CloudWatch
4. AWS DynamoDB
5. AWS SNS

## AWS IAM
IAM is an acronym for Identity and Access Management. By using AWS IAM, one can specify who or what can access services and resources in AWS and analyze access to refine permissions across AWS.

## AWS Lambda
Lambda is an event-driven, serverless computing platform provided by AWS. It is a computing service that runs code in response to events and automatically manages the computing resources required by that code.

## AWS CloudWatch
CloudWatch is a monitoring services that collects monitoring and operational data in the form of logs, metrics, and events, and visualizes it using automated dashboards so you can get a unified view of your AWS resources, applications, and services that run on AWS and on premises.

## AWS DynamoDB
Amazon DynamoDB is a fully managed, serverless, key-value NoSQL database designed to run high-performance applications at any scale.

## AWS SNS
Amazon Simple Notification Service (SNS) sends notifications two ways, A2A and A2P. A2A provides allows it to talk to other services while A2P functionality lets you send messages to your customers with SMS texts, push notifications, and email. 
from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    RemovalPolicy,
    aws_events as event_,
    aws_events_targets as target_,
    aws_cloudwatch as cloudwatch_,
    aws_iam as iam_,
    aws_sns as sns_,
    aws_cloudwatch_actions as cwactions_,
    aws_sns_subscriptions as subscriptions_,
    aws_dynamodb as db_,
    aws_codedeploy as codedeploy_,
    aws_apigateway as gate_
)
from constructs import Construct
from resources import constants as constant
import os as os_
import boto3 as boto_


class FarazSprint4Stack(Stack):
    '''
        These line of codes are acting as Infrastructure as a Code (IaaC).
        They allocate a VM on cloud for our Lambda function.
    '''
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Calling role funtion that will give Lambda "full cloudwatch access"
        lambda_role = self.apiLambdaRole()
        # Creating my API Lambda
        API_lambda = self.create_lambda("apiLambda", "./resources", "apiLambda.lambda_handler", lambda_role)
        # Applying removal policy to destroy instance
        API_lambda.apply_removal_policy(RemovalPolicy.DESTROY)

        #REST API
        api = gate_.LambdaRestApi(self, "FarazAPI",
            handler = API_lambda,
            proxy = False
            )
        
        urls = api.root.add_resource("urls")
        # POST (U/Update from CRUD)
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/IResource.html#aws_cdk.aws_apigateway.IResource
        urls.add_method("POST")
        
        # PUT (C/Create from CRUD)
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/IResource.html#aws_cdk.aws_apigateway.IResource
        urls.add_method("PUT")

        # GET (R/Read from CRUD)
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/IResource.html#aws_cdk.aws_apigateway.IResource
        urls.add_method("GET")

        # DELETE (D/Delete from CRUD)
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/IResource.html#aws_cdk.aws_apigateway.IResource
        urls.add_method("DELETE")

        # Calling role funtion that will give Lambda "full cloudwatch access"
        lambda_role = self.FWHLambdaRole()
        # Calling my create_lambda function
        FWH_lambda = self.create_lambda("FWHLambda", "./resources", "FWHLambda.lambda_handler", lambda_role)
        # Applying removal policy to destroy instance
        FWH_lambda.apply_removal_policy(RemovalPolicy.DESTROY)


        # Calling role funtion that will give Lambda "full dynamodb access"
        DB_lambda_role = self.DBLambdaRole()
        # Calling my create_lambda function
        DB_lambda = self.create_lambda("DBLambda", "./resources", "DBLambda.lambda_handler", DB_lambda_role)

        # Creating my DynamoBD table for Alarm Notifications
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/Table.html
        AlarmTable = self.create_table("AlarmNotificationTable", "ID")
        AlarmTable_name = AlarmTable.table_name
        DB_lambda.add_environment("AlarmTable", AlarmTable_name)

        # Granting full read/write access to my table
        AlarmTable.grant_full_access(DB_lambda)

        # Creating my DynamoBD table for URLs
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/Table.html
        urlTable = self.create_table("URLTable", "BODY")
        urlTable_name = urlTable.table_name
        API_lambda.add_environment("urlTable", urlTable_name)

        # Adding urlTable name to Web health lambda
        FWH_lambda.add_environment("urlTable", urlTable_name)

        # Granting API_lambda full read/write access to my url table
        urlTable.grant_full_access(API_lambda)
        # Granting FWH_lambda full read/write access to my url table
        urlTable.grant_full_access(FWH_lambda)

        # Defining an event that will invoke our Lambda on scheule time i.e. 1 minute
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_events/Rule.html
        schedule = event_.Schedule.cron()
        target = target_.LambdaFunction(handler = FWH_lambda)
        rule = event_.Rule(self, "ScheduleRule",
            schedule = schedule,
            targets = [target]
        )
        rule.apply_removal_policy(RemovalPolicy.DESTROY)

        # Creating Topic (message server)
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns/Topic.html
        topic = sns_.Topic(self, "AlarmNotification")
        topicARN = topic.topic_arn
        # Adding environmnet variable to access topic from lambda
        FWH_lambda.add_environment("snsARN", topicARN)
        topic.apply_removal_policy(RemovalPolicy.DESTROY)

        # Connecting my Topic (message server) with subscribers
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns_subscriptions.html
        topic.add_subscription(subscriptions_.EmailSubscription("muhammad.faraz.skipq@gmail.com"))

        # Connecting my Topic (message server) with subscribers
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns_subscriptions/LambdaSubscription.html
        topic.add_subscription(subscriptions_.LambdaSubscription(DB_lambda))

        # Dimension for durationMetric 
        dimensions = {'functionName' : FWH_lambda.function_name}

        # creating matric for Duration alarm
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Metric.html
        durationMetric = cloudwatch_.Metric(metric_name = "DurationMatric", 
            namespace = "AWS/Lambda", 
            dimensions_map = dimensions, 
            period = Duration.minutes(1)
            )

        # Creating my InvocationsMetric
        invocationMetric = FWH_lambda.metric_invocations()

        # creating matric for Duration Alarm
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
        durationAlarm = cloudwatch_.Alarm(self, "DurationAlarm",
                comparison_operator = cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                threshold = 1,
                evaluation_periods = 1,
                metric = durationMetric,
                datapoints_to_alarm = 1
                )
        # creating matric for invocation Alarm
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
        invocationAlarm = cloudwatch_.Alarm(self, "InvocationAlarm",
                comparison_operator = cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                threshold = 1,
                evaluation_periods = 1,
                metric = invocationMetric,
                datapoints_to_alarm = 1
                )

        # Creating Alias for web health lambda
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Alias.html#aws_cdk.aws_lambda.Alias
        version = FWH_lambda.current_version
        alias = lambda_.Alias(self, "LambdaAlias",
                alias_name = "Prod",
                version = version)

        # For version Roll back
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codedeploy/LambdaDeploymentGroup.html
        deployement_group = codedeploy_.LambdaDeploymentGroup(self, "BlueGreenDeployement",
                alias = alias,
                alarms = [durationAlarm, invocationAlarm],
                # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codedeploy/LambdaDeploymentGroup.html
                deployment_config = codedeploy_.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE)

    
    # Defining role for my lambda function
    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/Role.html
    def apiLambdaRole(self):
        '''
            This will give out Lambda full access to publish on cloudwatch
        '''
        apiLambda_role = iam_.Role(self, "apiLambda Role",
            assumed_by = iam_.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies = [
                    iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayInvokeFullAccess")
            ])
        return apiLambda_role


    # Defining role for my lambda function
    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/Role.html
    def FWHLambdaRole(self):
        '''
            This will give out Lambda full access to publish on cloudwatch
        '''
        FWHLambda_role = iam_.Role(self, "FWHLambda Role",
            assumed_by = iam_.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies = [
                    iam_.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                    iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess")
            ])
        return FWHLambda_role

    # Defining role for my DynamoDB
    # https://us-east-1.console.aws.amazon.com/iamv2/home?region=us-east-1#/policies
    def DBLambdaRole(self):
        '''
            This will give out DynamoDB full access
        '''
        DBLambda_role = iam_.Role(self, "DBLambda Role",
            assumed_by = iam_.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies = [
                    iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess")
            ])
        return DBLambda_role

    # Defining my create_lembda function
    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/README.html
    def create_lambda(self, id_, path, handler, role):
        '''
            This will take my desired action of Lambda function performing code 
            and will deploy it on cloud
        '''
        return lambda_.Function(self,
            id = id_,
            code = lambda_.Code.from_asset(path),
            handler = handler,
            runtime = lambda_.Runtime.PYTHON_3_8,
            role = role,
            timeout = Duration.seconds(30)
        )
    
    # Defining DynamoDB table
    def create_table(self, id_, key):
        return db_.Table(self,
            id = id_,
            removal_policy = RemovalPolicy.DESTROY,
            partition_key = db_.Attribute(name = key, type = db_.AttributeType.STRING)
            )
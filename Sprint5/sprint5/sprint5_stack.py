from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    RemovalPolicy,
    aws_apigateway as gate_,
    aws_iam as iam_,
    aws_sns as sns_,
    aws_sns_subscriptions as subscriptions_,
)
from constructs import Construct

class FarazSprint5D1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Calling role funtion that will give Lambda "full cloudwatch access"
        lambda_role = self.apiLambdaRole()
        # Creating my API Lambda
        API_lambda = self.create_lambda("apiLambda", "./resources", "apiLambda.lambda_handler", lambda_role)
        # Applying removal policy to destroy instance
        API_lambda.apply_removal_policy(RemovalPolicy.DESTROY)

        #REST API
        api = gate_.LambdaRestApi(self, "FarazD1API",
            handler = API_lambda,
            proxy = False
            )
        
        Eresponse = api.root.add_resource("Eresponse")
        # PUT (C/Create from CRUD)
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/IResource.html#aws_cdk.aws_apigateway.IResource
        Eresponse.add_method("PUT")

        # Creating Topic (message server)
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns/Topic.html
        topic = sns_.Topic(self, "AlarmNotification")
        topicARN = topic.topic_arn
        # Adding environmnet variable to access topic from lambda
        API_lambda.add_environment("snsARN", topicARN)
        topic.apply_removal_policy(RemovalPolicy.DESTROY)

        # Connecting my Topic (message server) with subscribers
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns_subscriptions.html
        topic.add_subscription(subscriptions_.EmailSubscription("muhammad.faraz.skipq@gmail.com"))   

    # Defining role for my lambda function
    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/Role.html
    def apiLambdaRole(self):
        '''
            This will give out Lambda full access to publish on cloudwatch
        '''
        apiLambda_role = iam_.Role(self, "apiLambda Role",
            assumed_by = iam_.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies = [
                    iam_.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                    iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayInvokeFullAccess")
            ])
        return apiLambda_role

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
from aws_cdk import (
    Stack,
    aws_lambda as lambda_
)
from constructs import Construct

class FarazSprint1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        hw_lambda = self.create_lambda("helloLambda", "./sprint1/recources", "helloLambda.lambda_handler")

    # Defining my create_lembda function
    # This will take my desired action performing code and will deploy it on cloud
    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/README.html
    def create_lambda(self, id_, path, handler):
        return lambda_.Function(self,
            id = id_,
            code = lambda_.Code.from_asset(path),
            handler = handler,
            runtime = lambda_.Runtime.PYTHON_3_8,
        )

import aws_cdk as cdk_
import aws_cdk.assertions as assertions_

from sprint4.sprint4_stack import FarazSprint4Stack

# This test will check if the timeout of lambda function is 15 seconds
def test_lambda_timeout():
    app = cdk_.App()
    stack = FarazSprint4Stack(app, "FarazSprint3Stack")
    template = assertions_.Template.from_stack(stack)

    template.has_resource_properties("AWS::Lambda::Function", {
        "Timeout": 30
    })

# This test will check if there are two lambda function in the app
def test_lambda_count():
    app = cdk_.App()
    stack = FarazSprint4Stack(app, "FarazSprint3Stack")
    template = assertions_.Template.from_stack(stack)

    template.resource_count_is("AWS::Lambda::Function", 3)

# This test will check if there 1 Dynamo DB table in the app
def test_dbtable_count():
    app = cdk_.App()
    stack = FarazSprint4Stack(app, "FarazSprint3Stack")
    template = assertions_.Template.from_stack(stack)

    template.resource_count_is("AWS::DynamoDB::Table", 2)


# This test will check if SNS is subscribed by an email
def test_subscription_email():
    app = cdk_.App()
    stack = FarazSprint4Stack(app, "FarazSprint3Stack")
    template = assertions_.Template.from_stack(stack)

    template.has_resource("AWS::SNS::Subscription", 
            {"Properties" : {"Protocol" : "email"}})

# This test will check if SNS is subscribed by an lambda
def test_subscription_lambda():
    app = cdk_.App()
    stack = FarazSprint4Stack(app, "FarazSprint3Stack")
    template = assertions_.Template.from_stack(stack)

    template.has_resource("AWS::SNS::Subscription", 
            {"Properties" : {"Protocol" : "lambda"}})

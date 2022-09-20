from math import pi
from aws_cdk import (
    # Duration
    Stack,
    pipelines as pipeline_,
    aws_codepipeline_actions as action_
)
from constructs import Construct
import aws_cdk as cdk_

from sprint3.pipelineStage import SP3Stage as stage_


class SP3PipelineStack(Stack):
    '''
        These line of codes are acting as Infrastructure as a Code (IaaC).
        They allocate a VM on cloud for our Lambda function.
    '''
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Defining my source directory
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/CodePipelineSource.html
        source_directory = pipeline_.CodePipelineSource.git_hub("faraz2022skipq/Pegasus_Python", "main",
                # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/SecretValue.html
                authentication = cdk_.SecretValue.secrets_manager("FarazSecret"),
                # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codepipeline_actions/GitHubTrigger.html#aws_cdk.aws_codepipeline_actions.GitHubTrigger
                trigger = action_.GitHubTrigger("POLL"))

        # Defining the ShellStep synthesizer that will run the commands of source directory
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/ShellStep.html
        synthesizer = pipeline_.ShellStep("Synth", 
                commands = ["cd faraz2022skipq/Sprint3/",
                            "npm install -g aws-cdk",
                            "pip install -r requirements.txt", "cdk synth"],
                input = source_directory,
                primary_output_directory = "faraz2022skipq/Sprint3/cdk.out")

        # Creating my pipeline
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/CodePipeline.html
        Farazpipeline = pipeline_.CodePipeline(self, "FarazPipeline", synth = synthesizer)


        # Pre-beta stages unit stesing testing
        unit_test = pipeline_.ShellStep("UnitTest",
                commands = ["cd faraz2022skipq/Sprint3/", 
                            "python3 -m pip install pytest", 
                            "pip install -r requirements.txt", "pytest"])

        # Beta stage
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/Stage.html
        beta = stage_(self, "FarazBetaStage")
        
        # gamma stage
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/Stage.html
        gamma = stage_(self, "FarazGammaStage")

        # Prod stage
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/Stage.html
        prod = stage_(self, "FarazProdStage")

        # Adding beta stage to pipeline
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/CodePipeline.html
        Farazpipeline.add_stage(beta, pre = [unit_test])

        # Defining my gamma stage
        Farazpipeline.add_stage(gamma)

        #Defining prod stage
                # Adding manual approval before further processing
                # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/ManualApprovalStep.html
        Farazpipeline.add_stage(prod, pre = [pipeline_.ManualApprovalStep("FarazApproval")])

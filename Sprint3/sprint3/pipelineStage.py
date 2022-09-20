from aws_cdk import (
    Stage,
)
from constructs import Construct
import aws_cdk as cdk_
from sprint3.sprint3_stack import FarazSprint3Stack


class SP3Stage(Stage):
    '''
        These line of codes are acting as Infrastructure as a Code (IaaC).
        They allocate a VM on cloud for our Lambda function.
    '''
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Directing my stages to my stack
        self.stage = FarazSprint3Stack(self, "FarazSprint3Stack")
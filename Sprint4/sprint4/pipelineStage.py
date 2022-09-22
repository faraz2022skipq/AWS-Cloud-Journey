from aws_cdk import (
    Stage,
)
from constructs import Construct
import aws_cdk as cdk_
from sprint4.sprint4_stack import FarazSprint4Stack


class SP4Stage(Stage):
    '''
        These line of codes are acting as Infrastructure as a Code (IaaC).
        They allocate a VM on cloud for our Lambda function.
    '''
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Directing my stages to my stack
        self.stage = FarazSprint4Stack(self, "FarazSprint4Stack")
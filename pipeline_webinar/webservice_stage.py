from aws_cdk import core
from os import path
from aws_cdk import aws_lambda as lmb
from aws_cdk import aws_apigateway as apigw
from .pipeline_webinar_stack import PipelineWebinarStack

class WebServiceStage(core.Stage):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        service = PipelineWebinarStack(self, 'Webservice')

        self.url_output = service.url_output
from aws_cdk import core
from os import path
from aws_cdk import aws_lambda as lmb
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_codedeploy as codedeploy

class PipelineWebinarStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        this_dir = path.dirname(__file__)
        handler = lmb.Function(self,'Handler',
            runtime=lmb.Runtime.PYTHON_3_7,
            handler='handler.handler',
            code=lmb.Code.from_asset(path.join(this_dir,'lambda'))
        )
        alias = lmb.Alias(self, 'HandlerAlias',
            alias_name='Current',
            version=handler.current_version)

        gw = apigw.LambdaRestApi(self,'Gateway for Lambda',
            description='Endpoint for CDK Lambda test',
            # handler=handler.current_version)
            handler=alias)

        codedeploy.LambdaDeploymentGroup(self, 'DeploymentGroup',
            alias=alias,
            deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE
        )

        self.url_output = core.CfnOutput(self, 'Url', value=gw.url)

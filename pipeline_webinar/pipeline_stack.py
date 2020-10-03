from aws_cdk import core
from aws_cdk import aws_codepipeline as cp
from aws_cdk import aws_codepipeline_actions as cpa
from aws_cdk import pipelines

from .webservice_stage import WebServiceStage

class PipelineStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # get source from Github
        source_artifact = cp.Artifact()
        cloud_assembly_artifact = cp.Artifact()

        pipeline = pipelines.CdkPipeline(self, 'Pipeline',
            cloud_assembly_artifact=cloud_assembly_artifact,
            pipeline_name='CDKWebinarPipeline',
            source_action=cpa.GitHubSourceAction(
                action_name='Github',
                output=source_artifact,
                oauth_token=core.SecretValue.secrets_manager(secret_id='dev/github-token', json_field='github-token'),
                owner='jvargh',
                repo='cdk-pipelines-webinar',
                trigger=cpa.GitHubTrigger.POLL),
            # Runs python code and creates cloud assembly
            synth_action=pipelines.SimpleSynthAction(
                source_artifact=source_artifact,
                cloud_assembly_artifact=cloud_assembly_artifact,
                install_command='npm install -g aws-cdk && pip install -r requirements.txt',
                build_command='pytest unittests',
                synth_command='cdk synth')
        )
        pre_prod_stage = pipeline.add_application_stage(app_stage=WebServiceStage(self,'Pre-Prod', env={
            'account': '524517701320',
            'region': 'us-east-1'
        }))
        pre_prod_stage.add_manual_approval_action(action_name='Promote_To_Prod')

        pipeline.add_application_stage(app_stage=WebServiceStage(self,'Prod', env={
            'account': '524517701320',
            'region': 'us-east-1'
        }))
from aws_cdk import core
from aws_cdk import aws_codepipeline as cp
from aws_cdk import aws_codepipeline_actions as cpa
from aws_cdk import pipelines

class PipelineStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # get source from Github
        source_artifact = cp.Artifact()
        cloud_assembly_artifact = cp.Artifact()

        pipelines.CdkPipeline(self, 'Pipeline',
            cloud_assembly_artifact=cloud_assembly_artifact,
            pipeline_name='CDKWebinarPipeline',
            source_action=cpa.GitHubSourceAction(
                action_name='Github',
                output=source_artifact,
                oauth_token=core.SecretValue.secrets_manager(secret_id='dev/github-token', json_field='github-token'),
                owner='jvargh',
                repo='cdk-pipelines-webinar',
                trigger=cpa.GitHubTrigger.POLL
            ),
            # Runs python code and creates cloud assembly
            synth_action=pipelines.SimpleSynthAction(
                source_artifact=source_artifact,
                cloud_assembly_artifact=cloud_assembly_artifact,
                install_command='npm install -g aws-cdk && pip install -r requirements.txt',
                synth_command='cdk synth'
            )
        )


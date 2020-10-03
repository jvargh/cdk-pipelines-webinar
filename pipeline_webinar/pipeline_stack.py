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

        pre_prod_app = WebServiceStage(self,'Pre-Prod', env={
            'account': '524517701320',
            'region': 'us-east-1'
        })
        pre_prod_stage = pipeline.add_application_stage(app_stage=pre_prod_app)
        # pre_prod_stage.add_manual_approval_action(action_name='Promote_To_Prod')

        # shell script using source_art folder to run cmds and using user_op will
        # populate env var SERVICE_URL with the o/p of apigw
        pre_prod_stage.add_actions(pipelines.ShellScriptAction(
            action_name='Integration_Script',
            run_order=pre_prod_stage.next_sequential_run_order(),
            additional_artifacts=[source_artifact],
            commands=['pip install -r requirements.txt', 'pytest integtests'],
            use_outputs={
                'SERVICE_URL': pipeline.stack_output(pre_prod_app.url_output)
            }
        ))

        pipeline.add_application_stage(app_stage=WebServiceStage(self,'Prod', env={
            'account': '524517701320',
            'region': 'us-east-1'
        }))
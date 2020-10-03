from aws_cdk import core
from pipeline_webinar.pipeline_webinar_stack import PipelineWebinarStack


def test_lambda_handler():
    # GIVEN
    app = core.App()

    # WHEN
    PipelineWebinarStack(app, 'Stack')

    # THEN
    # (1) adding stack to an empty app, (2) synth and getting cfn template out
    template = app.synth().get_stack_by_name('Stack').template
    # (3) get lambda fn out of the template
    functions = [resource for resource in template['Resources'].values()
                 if resource['Type'] == 'AWS::Lambda::Function']
    assert len(functions) == 1
    assert functions[0]['Properties']['Handler'] == 'handler.handler'

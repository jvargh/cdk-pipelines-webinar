#!/usr/bin/env python3

from aws_cdk import core

from pipeline_webinar.pipeline_webinar_stack import PipelineWebinarStack
from pipeline_webinar.pipeline_stack import PipelineStack


app = core.App()
# PipelineWebinarStack(app, "pipelines-webinar")
PipelineStack(app,"PipelineStack", env={
    'account': 'ACCT#',
    'region': 'us-east-1'
})

app.synth()

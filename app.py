#!/usr/bin/env python3

from aws_cdk import core

from pipeline_webinar.pipeline_webinar_stack import PipelineWebinarStack


app = core.App()
PipelineWebinarStack(app, "pipeline-webinar")

app.synth()

from aws_cdk import App, Stack
from constructs import Construct

# Import your stack class
from my_cdk_project.my_cdk_project_stack import MyCdkProjectStack

app = App()
MyCdkProjectStack(app, "MyCdkProjectStack")

app.synth()

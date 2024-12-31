# from aws_cdk import (
#     Stack,
#     RemovalPolicy,
#     aws_s3 as s3,
#     aws_lambda as _lambda,
#     aws_iam as iam,
#     Duration
# )
# from constructs import Construct

# class MyCdkProjectStack(Stack):
#     def __init__(self, scope: Construct, id: str, **kwargs):
#         super().__init__(scope, id, **kwargs)

#         # Example S3 Bucket with removal policy
#         bucket = s3.Bucket(
#             self, "MyBucket",
#             removal_policy=RemovalPolicy.DESTROY  # Corrected reference
#         )

#         # Example Lambda function with IAM role
#         lambda_role = iam.Role(
#             self, "MyLambdaRole",
#             assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
#         )

#         _lambda.Function(
#             self, "MyLambdaFunction",
#             runtime=_lambda.Runtime.PYTHON_3_8,
#             handler="lambda.handler",
#             code=_lambda.Code.from_asset("lambda"),
#             environment={
#                 "BUCKET_NAME": bucket.bucket_name
#             },
#             role=lambda_role
#         )

from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_lambda as _lambda,
    Duration
)
from constructs import Construct

class MyCdkProjectStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Step 1: Create the S3 bucket
        bucket = s3.Bucket(
            self, "MyBucket",
            removal_policy=RemovalPolicy.DESTROY
        )

        # Step 2: Create a VPC (required for EC2 instance)
        vpc = ec2.Vpc(self, "MyVpc", max_azs=2)

        # Step 3: Create an EC2 instance
        instance_role = iam.Role(
            self, "MyInstanceRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        )

        # Grant the EC2 instance permissions to access the S3 bucket
        bucket.grant_read_write(instance_role)

        # Attach an Amazon SSM managed policy for easier instance management
        instance_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
        )

        # User data script to configure the EC2 instance
        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "#!/bin/bash",
            "sudo yum update -y",
            "sudo yum install -y nginx",
            "sudo systemctl enable nginx",
            "sudo systemctl start nginx",
            "echo 'Welcome to NGINX on EC2' > /usr/share/nginx/html/index.html",
            "hostnamectl set-hostname MyCustomHostname"
        )

        # Launch the EC2 instance
        instance = ec2.Instance(
            self, "MyInstance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=vpc,
            role=instance_role,
            user_data=user_data
        )

        # Step 4: Optional integration of the S3 bucket with EC2 instance
        # (Instance can access the S3 bucket directly via AWS CLI or SDK)

        # Example Lambda function with S3 bucket environment variable
        lambda_role = iam.Role(
            self, "MyLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )

        _lambda.Function(
            self, "MyLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "BUCKET_NAME": bucket.bucket_name
            },
            role=lambda_role
        )

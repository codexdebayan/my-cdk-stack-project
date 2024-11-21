from aws_cdk import (
    core as cdk,
    aws_s3 as s3,
    aws_kms as kms
)

class S3BucketStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a KMS key for encryption
        kms_key = kms.Key(
            self, "BucketKey",
            enable_key_rotation=True
        )

        # Create the S3 bucket
        bucket = s3.Bucket(
            self, "YourBucketLogicalID",
            # Bucket Name : 'mybucketcreationfromthecdk-6203'
            bucket_name="mybucketcreationfromthecdk-6203",
            versioned=True,
            encryption=s3.BucketEncryption.KMS,
            encryption_key=kms_key,
            lifecycle_rules=[
                s3.LifecycleRule(
                    transitions=[
                        s3.Transition(
                            storage_class=s3.StorageClass.INFREQUENT_ACCESS,
                            transition_after=cdk.Duration.days(30)
                        ),
                        s3.Transition(
                            storage_class=s3.StorageClass.GLACIER,
                            transition_after=cdk.Duration.days(90)
                        )
                    ]
                )
            ]
        )
        
        cdk.CfnOutput(
            self, "BucketName",
            value=bucket.bucket_name
        )


# Define the app
app = cdk.App()
S3BucketStack(app, "S3BucketStack")
app.synth()

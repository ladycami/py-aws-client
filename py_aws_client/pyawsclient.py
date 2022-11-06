import boto3
from typing import Optional

from py_aws_client.clients.s3 import S3
from py_aws_client.clients.iam import Iam
from py_aws_client.clients.ses import Ses
from py_aws_client.clients.sqs import Sqs
from py_aws_client.clients.sns import Sns
from py_aws_client.clients.ssm import Ssm
from py_aws_client.clients.ec2 import Ec2
from py_aws_client.clients.glue import Glue
from py_aws_client.clients.elbv2 import Elbv2
from py_aws_client.clients.config import Config
from py_aws_client.clients.dynamodb import DynamoDb
from py_aws_client.clients.asg import AutoscalingGroup
from py_aws_client.clients.cloudwatch import Cloudwatch
from py_aws_client.clients.cloudtrail import Cloudtrail
from py_aws_client.clients.secrets_manager import SecretsManager


class PyAwsClient(object):
    """
    The PyAwsClient is responsible for constructing various AWS API service Clients
    """
    _session: boto3.session.Session

    _region: str
    _profile_name: str

    def __init__(self, region: str, profile_name: Optional[str] = ''):
        """
        Initializes a new PyAwsClient
        The client will always create a client with the profile, when the profile is given
        Otherwise the client will create a default client using only the region.
        The default client will use the default AWS credentials.
        param region: The aws region to create new client in
        param profile_name: The aws profile to use when interacting against AWS.
        """
        self._region = region
        self._profile_name = profile_name

        if profile_name:
            self._session = boto3.session.Session(
                region_name=region,
                profile_name=profile_name,
            )

    def _get_client(self, client_type: type):
        if self._profile_name:
            return client_type(session=self._session)

        return client_type(region=self._region)

    def asg(self) -> AutoscalingGroup:
        """
        Creates a new AutoScaling Client
        """
        return self._get_client(AutoscalingGroup)

    def cloudwatch(self) -> Cloudwatch:
        """
        Creates a new Cloudwatch
        """
        return self._get_client(Cloudwatch)

    def ec2(self) -> Ec2:
        """
        Creates a new Ec2
        """
        return self._get_client(Ec2)

    def ses(self) -> Ses:
        """
        Creates a new Ses
        """
        return self._get_client(Ses)

    def ssm(self) -> Ssm:
        """
        Creates a new Ssm
        """
        return self._get_client(Ssm)

    def s3(self) -> S3:
        """
        Creates a new S3
        """
        return self._get_client(S3)

    def secretsmanager(self) -> SecretsManager:
        """
        Creates a new SecretsManager
        """
        return self._get_client(SecretsManager)

    def sqs(self) -> Sqs:
        """
        Creates a new Sqs
        """
        return self._get_client(Sqs)

    def sns(self) -> Sns:
        """
        Creates a new Sns
        """
        return self._get_client(Sns)

    def elbv2(self) -> Elbv2:
        """
        Creates a new Elbv2 (Application Load Balancer)
        """
        return self._get_client(Elbv2)

    def iam(self) -> Iam:
        """
        Creates a new IAM client
        """
        return self._get_client(Iam)

    def glue(self) -> Glue:
        """
        Creates a new Glue client
        """
        return self._get_client(Glue)

    def dynamodb(self) -> DynamoDb:
        """
        Creates a new DynamoDB client
        """
        return self._get_client(DynamoDb)

    def config(self) -> Config:
        """
        Creates a new Config client
        """
        return self._get_client(Config)

    def cloudtrail(self) -> Cloudtrail:
        """
        Creates a new Cloudtrail client
        """
        return self._get_client(Cloudtrail)

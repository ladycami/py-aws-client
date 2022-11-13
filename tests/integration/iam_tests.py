from pprint import pprint
from unittest import TestCase
from py_aws_client.pyawsclient import PyAwsClient


class IamTestCase(TestCase):
    def setUp(self):
        self.region = 'us-east-1'
        self.aws_client = PyAwsClient(
            region=self.region,
        )
        self.iam = self.aws_client.iam()



from pprint import pprint
from unittest import TestCase
from py_aws_client.pyawsclient import PyAwsClient


class CloudwatchTestCase(TestCase):
    def setUp(self):
        self.region = 'us-east-1'
        self.aws_client = PyAwsClient(
            region=self.region,
        )
        self.cloudwatch = self.aws_client.cloudwatch()



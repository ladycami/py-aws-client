from pprint import pprint
from unittest import TestCase
from py_aws_client.pyawsclient import PyAwsClient


class AsgTestCase(TestCase):
    def setUp(self):
        self.region = 'us-east-1'
        self.aws_client = PyAwsClient(
            region=self.region,
        )
        self.asg = self.aws_client.asg()



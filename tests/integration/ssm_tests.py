from pprint import pprint
from unittest import TestCase
from py_aws_client.pyawsclient import PyAwsClient


class SsmTestCase(TestCase):
    def setUp(self):
        self.region = 'us-east-1'
        self.aws_client = PyAwsClient(
            region=self.region,
        )
        self.ssm = self.aws_client.ssm()

    def test_get_parameter(self):
        response = self.ssm.get_parameter(
            parameter_name='/discord/mythal/token',
            with_decryption=True
        )

        print(response)
        return response

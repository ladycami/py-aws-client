import boto3
from moto import mock_ssm
from unittest import TestCase, main


class SsmTest(TestCase):
    mock_ssm = mock_ssm()
    parameter_name = '/systems/account_id'

    def setUp(self):
        self.mock_ssm.start()
        self.ssm = boto3.client('ssm')


if __name__ == '__main__':
    main()

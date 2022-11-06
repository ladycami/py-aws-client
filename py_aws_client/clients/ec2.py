import boto3
from typing import List, Dict


class Ec2(object):
    def __init__(self, session: boto3.session.Session = None, region: str = None):
        """
        Creates a client using either the boto3 Session or region.
        param session: required when no region is provided
        param region: required when no session is provided
        """
        if session and region:
            raise EnvironmentError('1 of session or region must be provided')

        if session:
            self.client = session.client(
                service_name='ec2',
            )
        elif region:
            self.client = boto3.client(
                service_name='ec2',
                region_name=region
            )

    def get_instances(self, instance_ids: List[str] = None, filters: List[Dict] = None) -> Dict[str, any]:
        """
        Get instance information for ec2 instances

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances
        :param instance_ids: a list of instance ids to get
        :param filters: a list of filters to limit instances in the response
        :return: ec2 client describe instances response
        """
        describe_response = self.client.describe_instances(
            InstanceIds=instance_ids if instance_ids else [],
            Filters=filters if filters else [],
        )

        return describe_response

    def wait_for_instances_to_stop(self, instance_ids: List[str]) -> None:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Waiter.InstanceStopped
        :param instance_ids: a list of ec2 instance ids to wait for until stopped
        """
        waiter = self.client.get_waiter('instance_stopped')
        waiter.wait(
            InstanceIds=instance_ids,
            WaiterConfig={
                'Delay': 10,
                'MaxAttempts': 60
            }
        )

    def stop_instances(self, instance_ids: List[str], force: bool = False, wait: bool = True) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.stop_instances
        param instance_ids: a list of ec2 instance ids to stop
        param force: should the instances be forcefully stopped?  This is not graceful.
        param wait: do we want to wait for the instances to stop?
        :return:
        """
        response = self.client.stop_instances(
            InstanceIds=instance_ids,
            Force=force
        )

        if wait:
            self.wait_for_instances_to_stop(
                instance_ids=instance_ids
            )

        return response

    def reboot_instance(self, instance_ids: List[str]) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.reboot_instances
        :param instance_ids: EC2 instance ID
        """
        response = self.client.reboot_instances(
            InstanceIds=instance_ids
        )

        return response

    def describe_images(self, image_ids: List[str]) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_images
        :param image_ids: list of image ids to describe
        :return: describe images response
        """
        response = self.client.describe_images(
            ImageIds=image_ids
        )

        return response

    def wait_for_images_to_be_available(self, image_ids: List[str]) -> None:
        """
        Wait for Amazon Machine Images to become available for consumption/use.

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Waiter.ImageAvailable
        :param image_ids: list of image ids to wait on for availability
        """
        waiter = self.client.get_waiter('image_available')
        waiter.wait(
            ImageIds=image_ids,
            WaiterConfig={
                'Delay': 15,
                'MaxAttempts': 720  # Timeout after 3 hours
            }
        )

    def create_image(self, instance_id: str, name: str, description: str,
                     no_reboot: bool = False, tag_specifications: list = None, wait: bool = True) -> Dict[str, any]:
        """
        Creates an Amazon Machine Image from the given instance id.

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.create_image
        param instance_id: instance id to create an image from
        param name: unique name to give the ami
        param description: how would you describe this ami?
        param no_reboot: when True, the AMI is not rebooted when the image is created.
        param tag_specifications: list of tag specs for the resulting snapshot and image.
        param wait: do we want to wait until the image is available?
        :return: create image response
        """
        if not tag_specifications:
            tag_specifications = []

        response = self.client.create_image(
            InstanceId=instance_id,
            Name=name,
            Description=description,
            NoReboot=no_reboot,
            TagSpecifications=tag_specifications
        )

        if wait:
            image_id = response.get('ImageId')
            self.wait_for_images_to_be_available(
                image_ids=[image_id]
            )

        return response

    def describe_latest_launch_template_version(self, launch_template_id: str) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_launch_template_versions
        :param launch_template_id: id of the launch template to get the latest version of.
        :return:
        """
        response = self.client.describe_launch_template_versions(
            LaunchTemplateId=launch_template_id,
            Versions=[
                '$Latest',
            ]
        )

        return response

    def describe_instance_status(self, instance_ids: List[str]) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instance_status
        :param instance_ids:
        :return:
        """
        response = self.client.describe_instance_status(
            InstanceIds=instance_ids
        )

        return response

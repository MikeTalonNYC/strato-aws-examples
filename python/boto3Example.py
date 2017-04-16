#!/usr/bin/env python

import boto3
import sys


def main(args):

    # This script shows and example of Boto3 integration with Stratoscale Symphony
    # The scenario is as such:
    # 1. Instantiate an instance from an AMI
    # 2. Create a 20 GB volume
    # 3. Attach the volume to the created AMI.

    # Creating connection to Symphony AWS Compatible region
    client = boto3.Session.client(boto3.session.Session(), service_name="ec2", region_name="symphony",
                                  endpoint_url="http://<cluster ip>/api/v2/ec2/",
                                  aws_access_key_id="<key>",
                                  aws_secret_access_key="<secret>")

    # Finding our centos image, grabbing it's image id.
    images = client.describe_images()
    for image in images['Images']:
        if 'centos' in image['Name']:
            image_id = image['ImageId']

    print "Found desired image with id: " + image_id

    # Running a new instance using our centos image id
    ec2_instance = client.run_instances(
        ImageId=image_id,
        MinCount=1,
        MaxCount=1
    )

    # Check if ec2 instance was created successfully
    if ec2_instance['ResponseMetadata']['HTTPStatusCode'] is 200:
        print "Successfully created instance! " + ec2_instance['Instances'][0]['InstanceId']

    # Create an ebs volume, 20G size
    ebs_vol = client.create_volume(
        Size=20,
        AvailabilityZone='symphony'
    )

    # Check that the EBS volume had been created successfully
    if ebs_vol['ResponseMetadata']['HTTPStatusCode'] is 200:
        print "Successfully created Volume! " + ebs_vol['VolumeId']

    volumeId = ebs_vol['VolumeId']

    # Attaching EBS volume to our ec2 instance
    attach_resp = client.attach_volume(
        VolumeId=ebs_vol['VolumeId'],
        InstanceId=ec2_instance['Instances'][0]['InstanceId'],
        Device='/dev/sdm'
    )

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


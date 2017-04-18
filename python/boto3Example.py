import boto3
import sys


def main():
    """
    This script shows and example of Boto3 integration with Stratoscale Symphony.

    The scenario is as such:
         1. Instantiate an instance from an AMI,
         2. Create a 20 GB volume,
         3. Attach the volume to the created AMI.
    """

    # creating a connection to Symphony AWS Compatible region
    client = boto3.Session.client(boto3.session.Session(), service_name="ec2", region_name="symphony",
                                  endpoint_url="http://<cluster ip>/api/v2/ec2/",
                                  aws_access_key_id="<key>",
                                  aws_secret_access_key="<secret>")

    # finding our Centos image, grabbing its image ID
    images = client.describe_images()
    image_id = next(image['ImageId'] for image in images if 'centos' in image['Name'])

    print "Found desired image with ID: " + image_id

    # running a new instance using our Centos image ID
    ec2_instance = client.run_instances(
        ImageId=image_id,
        MinCount=1,
        MaxCount=1
    )

    # check if EC2 instance was created successfully
    if ec2_instance['ResponseMetadata']['HTTPStatusCode'] == 200:
        print "Successfully created instance! " + ec2_instance['Instances'][0]['InstanceId']

    # create an EBS volume, 20G size
    ebs_vol = client.create_volume(
        Size=20,
        AvailabilityZone='symphony'
    )

    volume_id = ebs_vol['VolumeId']

    # check that the EBS volume had been created successfully
    if ebs_vol['ResponseMetadata']['HTTPStatusCode'] == 200:
        print "Successfully created Volume! " + volume_id

    # attaching EBS volume to our EC2 instance
    attach_resp = client.attach_volume(
        VolumeId=volume_id,
        InstanceId=ec2_instance['Instances'][0]['InstanceId'],
        Device='/dev/sdm'
    )

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
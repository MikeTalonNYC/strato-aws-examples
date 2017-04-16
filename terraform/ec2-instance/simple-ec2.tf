provider "aws" {
    access_key = "<key>"
    secret_key = "<secret>"

    endpoints {
        ec2 = "http://<cluster vip>/api/v2/ec2"
    }   

    insecure = "true"
    skip_metadata_api_check = true
    skip_credentials_validation = true
    region = "eu-west-1"
}

resource "aws_instance" "web" {
    ami = "<ami identifier>"
    instance_type = "m1.small" # or any other AWS instance type
}

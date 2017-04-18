#! /bin/bash
docker run -d -p 5000:5000 --name registry -v ./config-symphony.yml:/etc/docker/registry/config.yml registry:2

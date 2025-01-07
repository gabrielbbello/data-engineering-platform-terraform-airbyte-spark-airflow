#!/bin/bash
sudo yum update -y

sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

DOCKER_CONFIG=${DOCKER_CONFIG:-/usr/local/lib/docker}
sudo mkdir -p $DOCKER_CONFIG/cli-plugins
sudo curl -SL https://github.com/docker/compose/releases/download/v2.16.0/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
sudo chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose

sudo ln -s $DOCKER_CONFIG/cli-plugins/docker-compose /usr/local/bin/docker-compose

echo 'export PATH=$PATH:/usr/local/bin' >> /home/ec2-user/.bashrc

sudo yum install -y git

git config --global user.name "Gabriel Bello"
git config --global user.email "gabriel.bello@cognitivo.ai"

sudo -u ec2-user git clone --branch v0.44.4 https://github.com/airbytehq/airbyte.git /home/ec2-user/airbyte
cd /home/ec2-user/airbyte
sudo -u ec2-user chmod +x run-ab-platform.sh

sudo -u ec2-user bash -c "source /home/ec2-user/.bashrc && /home/ec2-user/airbyte/run-ab-platform.sh -b"
terraform {
  required_version = "1.9.4"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
}

provider "aws" {
  region  = var.region
  profile = var.profile
}

data "aws_availability_zones" "available" {}

resource "random_id" "global" {
  byte_length = 8
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "2.77.0"

  name                 = "bello-${random_id.global.hex}"
  cidr                 = "10.0.0.0/16"
  azs                  = data.aws_availability_zones.available.names
  public_subnets       = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]
  enable_dns_hostnames = true
  enable_dns_support   = true
}

module "s3" {
  source   = "./resource.aws.s3"
  for_each = toset(var.bucket_names)
  name     = "${each.value}-${random_id.global.hex}"

  tags = var.bucket_tags
}

resource "aws_db_subnet_group" "rds" {
  name       = "bello-${random_id.global.hex}"
  subnet_ids = module.vpc.public_subnets

  tags = {
    Email = "gabrielbbello@gmail.com"
  }
}

resource "aws_security_group" "rds" {
  name   = "bello-${random_id.global.hex}"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Email = "gabrielbbello@gmail.com"
  }
}

resource "aws_db_parameter_group" "rds" {
  name   = "bello-${random_id.global.hex}"
  family = "postgres16"

  parameter {
    name  = "log_connections"
    value = "1"
  }
}

resource "aws_db_instance" "rds" {
  identifier             = "bello-${random_id.global.hex}"
  instance_class         = "db.t3.micro"
  allocated_storage      = 5
  engine                 = "postgres"
  engine_version         = "16.5"
  username               = "bello"
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.rds.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  parameter_group_name   = aws_db_parameter_group.rds.name
  publicly_accessible    = true
  skip_final_snapshot    = true
}

resource "aws_instance" "this" {
  ami                    = "ami-0182f373e66f89c85"
  instance_type          = "t2.medium"
  subnet_id              = module.vpc.public_subnets[0]
  vpc_security_group_ids = [aws_security_group.airbyte.id]
  key_name               = var.ssh_key_name

  user_data = file("${path.module}/../../scripts/airbyte_setup.sh")

  tags = {
    Name      = "bello-airbyte-${random_id.global.hex}"
    ManagedBy = "Terraform"
    CreatedBy = "gabrielbbello@gmail.com"
  }

}

resource "aws_key_pair" "this" {
  key_name   = var.ssh_key_name
  public_key = file(var.ssh_key_path)
}


resource "aws_security_group" "airbyte" {
  name   = "bello_airbyte_sg"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
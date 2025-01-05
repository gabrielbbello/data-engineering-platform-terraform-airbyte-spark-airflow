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
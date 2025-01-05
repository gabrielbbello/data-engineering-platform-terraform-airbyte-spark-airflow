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
  region  = "us-east-1"
  profile = "cog-dev-bello-terraform"
}

data "aws_availability_zones" "available" {}

resource "random_id" "global" {
  byte_length = 8
}
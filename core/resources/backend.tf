terraform {
  backend "s3" {
    bucket         = "bello-tf-state-backend"
    key            = "tf-state/terraform.tfstate"
    region         = "us-east-1"
    profile        = "cog-dev-bello-terraform"
    encrypt        = true
    dynamodb_table = "bello_terraform_state"
  }
}
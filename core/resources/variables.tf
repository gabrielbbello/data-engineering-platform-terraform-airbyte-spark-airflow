variable "region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "profile" {
  description = "AWS CLI profile to use"
  type        = string
  default     = "default"
}

variable "bucket_names" {
  description = "Buckets name list for Datalake"
  type        = list(string)
  default     = ["project-bello-bronze-layer", "project-bello-silver-layer", "project-bello-gold-layer"]
}

variable "bucket_tags" {
  description = "Standard tags for every bucket"
  type        = map(string)
  default = {
    ManagedBy = "Terraform"
    CreatedBy = "gabrielbbello@gmail.com"
  }
}

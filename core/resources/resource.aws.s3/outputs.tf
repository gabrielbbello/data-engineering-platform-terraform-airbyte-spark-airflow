output "name" {
  description = "Bucket domain name"
  value       = aws_s3_bucket.this.bucket_domain_name
}

output "arn" {
  description = "Bucket ARN"
  value       = aws_s3_bucket.this.arn
}
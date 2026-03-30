# Output Variables
# These display useful information after Terraform applies the configuration

output "bucket_arn" {
  description = "ARN (Amazon Resource Name) of the S3 bucket"
  value       = aws_s3_bucket.static_website.arn
}

output "bucket_name" {
  description = "Name (ID) of the S3 bucket"
  value       = aws_s3_bucket.static_website.id
}

output "website_domain" {
  description = "Domain name of the S3 website"
  value       = aws_s3_bucket_website_configuration.static_website.website_domain
}

output "website_endpoint" {
  description = "Full URL endpoint to access the static website"
  value       = aws_s3_bucket_website_configuration.static_website.website_endpoint
}

output "localstack_url" {
  description = "LocalStack-specific URL for accessing the website"
  value       = "http://${var.bucket_name}.s3-website.localhost.localstack.cloud:4566/"
}

# Provider Configuration for LocalStack
# This configures Terraform to work with LocalStack instead of real AWS

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  required_version = ">= 1.0"
}

provider "aws" {
  access_key = "test"
  secret_key = "test"
  region     = "us-east-1"
  
  # Disable credential validation since we're using LocalStack
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  
  # Enable path-style S3 URLs (needed for some LocalStack configurations)
  s3_use_path_style = false
  
  # Point all AWS service endpoints to LocalStack
  endpoints {
    s3 = "http://s3.localhost.localstack.cloud:4566"
  }
}

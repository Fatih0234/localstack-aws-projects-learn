# Input Variables
# These allow you to customize the deployment without changing the main code

variable "bucket_name" {
  description = "Name of the S3 bucket. Must be globally unique (in real AWS) or unique within LocalStack."
  type        = string
  default     = "my-static-website-bucket"
}

variable "tags" {
  description = "Tags to set on the bucket for organization and identification."
  type        = map(string)
  default = {
    Project     = "LocalStack-AWS-Learning"
    Environment = "local"
    ManagedBy   = "Terraform"
  }
}

variable "index_document" {
  description = "Name of the index document (default page)"
  type        = string
  default     = "index.html"
}

variable "error_document" {
  description = "Name of the error document (404 page)"
  type        = string
  default     = "error.html"
}

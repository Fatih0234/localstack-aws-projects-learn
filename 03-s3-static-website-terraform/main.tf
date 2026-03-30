# Main Terraform Configuration
# This file defines all the AWS resources needed for the S3 static website

# Create the S3 bucket
resource "aws_s3_bucket" "static_website" {
  bucket = var.bucket_name
  tags   = var.tags
}

# Configure the bucket for static website hosting
resource "aws_s3_bucket_website_configuration" "static_website" {
  bucket = aws_s3_bucket.static_website.id

  index_document {
    suffix = var.index_document
  }

  error_document {
    key = var.error_document
  }
}

# Set bucket ownership controls (required for ACLs)
resource "aws_s3_bucket_ownership_controls" "static_website" {
  bucket = aws_s3_bucket.static_website.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

# Set public access block to allow public access (needed for static website)
resource "aws_s3_bucket_public_access_block" "static_website" {
  bucket = aws_s3_bucket.static_website.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# Set bucket ACL to public-read
resource "aws_s3_bucket_acl" "static_website" {
  depends_on = [
    aws_s3_bucket_ownership_controls.static_website,
    aws_s3_bucket_public_access_block.static_website,
  ]

  bucket = aws_s3_bucket.static_website.id
  acl    = "public-read"
}

# Set bucket policy to allow public read access
resource "aws_s3_bucket_policy" "static_website" {
  depends_on = [aws_s3_bucket_public_access_block.static_website]

  bucket = aws_s3_bucket.static_website.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource = [
          aws_s3_bucket.static_website.arn,
          "${aws_s3_bucket.static_website.arn}/*",
        ]
      },
    ]
  })
}

# Upload HTML files to the bucket
resource "aws_s3_object" "html_files" {
  for_each = fileset(path.module, "*.html")

  bucket       = aws_s3_bucket.static_website.id
  key          = each.value
  source       = each.value
  content_type = "text/html"
  etag         = filemd5(each.value)
  acl          = "public-read"
}

# Upload static assets (images, CSS, JS, etc.) to the bucket
resource "aws_s3_object" "assets" {
  for_each = fileset(path.module, "assets/*")

  bucket = aws_s3_bucket.static_website.id
  key    = each.value
  source = each.value
  etag   = filemd5(each.value)
  acl    = "public-read"
}

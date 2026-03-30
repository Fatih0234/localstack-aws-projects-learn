# Project 03: S3 Static Website with Terraform

[![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=flat&logo=terraform&logoColor=white)](https://www.terraform.io/)
[![AWS S3](https://img.shields.io/badge/AWS%20S3-569A31?style=flat&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/s3/)
[![LocalStack](https://img.shields.io/badge/LocalStack-AWS%20Emulation-blue)](https://localstack.cloud/)

> Learn Infrastructure as Code (IaC) by deploying a static website on S3 using Terraform with LocalStack

---

## Overview

This project demonstrates how to use **Terraform** to provision and manage **AWS S3** resources for hosting a static website locally using LocalStack. You'll learn Infrastructure as Code principles while building a practical, real-world deployment.

### What You'll Learn

- **Infrastructure as Code (IaC)** - Managing infrastructure through code
- **Terraform Basics** - Providers, resources, variables, and outputs
- **S3 Static Website Hosting** - Configuring buckets for web hosting
- **Bucket Policies & ACLs** - Controlling access to S3 resources
- **LocalStack Integration** - Using `tflocal` for local development

### Architecture

```
┌─────────────────┐
│   Browser       │
│   (User)        │
└────────┬────────┘
         │ HTTP Request
         ▼
┌──────────────────────────────┐
│   LocalStack S3              │
│   ┌─────────────────────┐    │
│   │   S3 Bucket         │    │
│   │   ┌───────────────┐ │    │
│   │   │  index.html   │ │    │
│   │   │  error.html   │ │    │
│   │   │  assets/      │ │    │
│   │   └───────────────┘ │    │
│   └─────────────────────┘    │
└──────────────────────────────┘
         ▲
         │ Terraform
┌────────┴────────┐
│  Terraform      │
│  Configuration  │
└─────────────────┘
```

---

## Prerequisites

### Required Software
- [Terraform](https://www.terraform.io/downloads.html) (1.0+)
- [LocalStack](https://docs.localstack.cloud/getting-started/)
- [awslocal](https://github.com/localstack/awscli-local) (optional, for verification)
- [tflocal](https://github.com/localstack/terraform-local) (optional wrapper)

### Verify Prerequisites
```bash
# Check Terraform version
terraform -version

# Check LocalStack status
localstack status
```

---

## Project Structure

```
03-s3-static-website-terraform/
├── assets/                    # Static assets (images, CSS, JS)
├── provider.tf               # LocalStack AWS provider configuration
├── variables.tf              # Input variables for customization
├── outputs.tf                # Output values after deployment
├── main.tf                   # Main resource definitions
├── index.html                # Website homepage
├── error.html                # 404 error page
└── README.md                 # This documentation
```

---

## AWS Resources Created

### S3 Bucket
- `aws_s3_bucket` - The main storage container
- `aws_s3_bucket_website_configuration` - Enables static website hosting
- `aws_s3_bucket_ownership_controls` - Configures bucket ownership
- `aws_s3_bucket_public_access_block` - Controls public access settings
- `aws_s3_bucket_acl` - Sets access control to public-read
- `aws_s3_bucket_policy` - Defines public read permissions

### S3 Objects
- `aws_s3_object` - Uploads HTML files and static assets

---

## Quick Start

### 1. Ensure LocalStack is Running

```bash
localstack start
```

Verify it's running:
```bash
localstack status
```

### 2. Initialize Terraform

Navigate to the project directory and initialize Terraform:

```bash
cd 03-s3-static-website-terraform
terraform init
```

**Or use tflocal (recommended):**
```bash
tflocal init
```

### 3. Review the Plan

Preview what Terraform will create:

```bash
terraform plan
```

**Or with tflocal:**
```bash
tflocal plan
```

### 4. Deploy the Infrastructure

Apply the configuration to create resources:

```bash
terraform apply
```

**Or with tflocal:**
```bash
tflocal apply
```

When prompted, type `yes` to confirm.

### 5. Access Your Website

After successful deployment, Terraform will output the website URL:

```
Outputs:

bucket_arn = "arn:aws:s3:::my-static-website-bucket"
bucket_name = "my-static-website-bucket"
localstack_url = "http://my-static-website-bucket.s3-website.localhost.localstack.cloud:4566/"
website_domain = "s3-website-us-east-1.amazonaws.com"
website_endpoint = "my-static-website-bucket.s3-website-us-east-1.amazonaws.com"
```

Open your browser and navigate to:
```
http://my-static-website-bucket.s3-website.localhost.localstack.cloud:4566/
```

Or use the `localstack_url` output from above.

---

## Testing Your Website

### Browser Testing
Open the LocalStack URL in your browser:
```
http://my-static-website-bucket.s3-website.localhost.localstack.cloud:4566/
```

You should see a styled welcome page with AWS branding.

### Test with curl
```bash
# Get the homepage
curl http://my-static-website-bucket.s3-website.localhost.localstack.cloud:4566/

# Test the 404 error page
curl http://my-static-website-bucket.s3-website.localhost.localstack.cloud:4566/nonexistent.html
```

### Verify with AWS CLI
```bash
# List bucket contents
awslocal s3 ls s3://my-static-website-bucket/

# Get bucket website configuration
awslocal s3api get-bucket-website --bucket my-static-website-bucket

# Check bucket policy
awslocal s3api get-bucket-policy --bucket my-static-website-bucket
```

---

## Customization

### Change Bucket Name
Edit `variables.tf` or provide a custom value:

```bash
terraform apply -var="bucket_name=my-custom-bucket-name"
```

### Add Custom Tags
```bash
terraform apply -var='tags={Project="MyProject",Owner="You",Environment="Dev"}'
```

### Upload Additional Assets
Place any files in the `assets/` folder and re-run `terraform apply`:
```bash
# Add an image
cp my-image.jpg assets/

# Re-apply to upload
tflocal apply
```

---

## Understanding the Code

### Provider Configuration (`provider.tf`)
- Points Terraform to LocalStack instead of AWS
- Uses mock credentials (`test/test`)
- Configures S3 endpoint to `s3.localhost.localstack.cloud:4566`

### Variables (`variables.tf`)
- `bucket_name` - Customize your bucket name
- `tags` - Add metadata to your resources
- `index_document` / `error_document` - Configure default pages

### Main Resources (`main.tf`)
1. **Bucket Creation** - Creates the S3 bucket
2. **Website Configuration** - Enables static hosting with index/error docs
3. **Ownership Controls** - Sets bucket object ownership
4. **Public Access** - Allows public access for website hosting
5. **Bucket ACL** - Sets public-read permissions
6. **Bucket Policy** - JSON policy allowing GetObject for everyone
7. **File Uploads** - Uploads HTML files and assets using `for_each`

### Outputs (`outputs.tf`)
- Bucket ARN and name for reference
- Website endpoint URLs for access
- LocalStack-specific URL format

---

## Cleanup

To destroy all created resources:

```bash
tflocal destroy
```

Or with terraform:
```bash
terraform destroy
```

Type `yes` to confirm. This removes the S3 bucket and all its contents.

---

## Troubleshooting

### LocalStack Not Running
```bash
localstack start
```

### Terraform Provider Issues
```bash
rm -rf .terraform .terraform.lock.hcl
terraform init
```

### Bucket Already Exists
Change the bucket name in `variables.tf` or use:
```bash
tflocal destroy  # Remove existing first
```

### Website Not Accessible
- Verify LocalStack is running: `localstack status`
- Check the correct endpoint URL in Terraform outputs
- Try using `localhost:4566` instead of the DNS name

---

## Key AWS Concepts

### S3 Static Website Hosting
- S3 can serve HTML, CSS, JavaScript, and images directly
- Requires public access configuration
- Uses special website endpoint URLs
- Supports custom index and error documents

### Bucket Policies vs ACLs
- **Bucket Policies** - JSON-based access control (more powerful)
- **ACLs** - Simpler, legacy access control method
- This project uses both for comprehensive access

### Infrastructure as Code
- **Declarative** - Define what you want, not how to get it
- **Version Control** - Track infrastructure changes in git
- **Reproducible** - Same configuration creates identical environments
- **Idempotent** - Running apply multiple times doesn't create duplicates

---

## Next Steps

- Try modifying the HTML/CSS and re-running `tflocal apply`
- Add CloudFront distribution (if using Pro features)
- Configure Route 53 for custom domain names
- Implement HTTPS with ACM certificates

---

## References

- [LocalStack S3 Tutorial](https://docs.localstack.cloud/aws/tutorials/s3-static-website-terraform/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS S3 Static Website Hosting](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html)
- [Terraform Basics](https://developer.hashicorp.com/terraform/tutorials/aws-get-started)

---

## License

MIT License - See main repository LICENSE file

---

**Happy Learning!** 🚀☁️

*Infrastructure as Code made simple with LocalStack and Terraform*

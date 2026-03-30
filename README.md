# LocalStack AWS Learning Projects

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![LocalStack](https://img.shields.io/badge/LocalStack-AWS%20Emulation-blue)](https://localstack.cloud/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> Hands-on AWS projects using LocalStack for safe, cost-free cloud learning

This repository contains practical projects designed to teach foundational AWS concepts through real-world implementations. All projects use **LocalStack** to emulate AWS services locally, allowing you to learn cloud concepts without incurring AWS costs or risking production environments.

---

## Projects Overview

| Project | AWS Services | Difficulty | Description |
|---------|--------------|------------|-------------|
| [01-quickstart-s3](./01-quickstart-s3/) | S3 | Beginner | Learn S3 basics: create buckets, upload/download files, list contents |
| [02-serverless-image-resizer](./02-serverless-image-resizer/) | S3, Lambda, SNS, SES, SSM | Intermediate | Complete serverless app with AI-powered image style transfer |
| [03-s3-static-website-terraform](./03-s3-static-website-terraform/) | S3, Terraform | Intermediate | Infrastructure as Code: Deploy S3 static website using Terraform |
| [04-ec2-basics](./04-ec2-basics/) | EC2, EBS, VPC | Intermediate | Launch VMs, configure networking, attach storage, manage lifecycles |

---

## Prerequisites

### Required Software
- [Python 3.11+](https://www.python.org/downloads/)
- [UV Package Manager](https://docs.astral.sh/uv/)
- [Docker](https://www.docker.com/) (for Lambda functions)
- [LocalStack](https://docs.localstack.cloud/getting-started/)
- [Terraform](https://www.terraform.io/downloads.html) (1.0+, for Project 03)

### AWS CLI Setup (for `awslocal` commands)
```bash
pip install awscli-local
```

---

## Quick Start

1. **Clone this repository**
   ```bash
   git clone https://github.com/Fatih0234/localstack-aws-projects-learn.git
   cd localstack-aws-projects-learn
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your LocalStack Auth Token
   ```

3. **Install dependencies**
   ```bash
   uv sync
   source .venv/bin/activate
   ```

4. **Start LocalStack**
   ```bash
   localstack start
   ```

5. **Verify it's running**
   ```bash
   localstack status
   awslocal s3 ls  # Should return empty list
   ```

---

## Project Structure

```
localstack-aws-projects-learn/
├── .venv/                          # Shared virtual environment
├── 01-quickstart-s3/             # S3 fundamentals project
│   ├── quickstart.py              # Main learning script
│   └── README.md                  # Project documentation
├── 02-serverless-image-resizer/   # Serverless image processing
│   ├── app/                        # Application code
│   │   ├── lambdas/                # 4 Lambda functions
│   │   ├── website/                # Frontend application
│   │   └── deployment/             # Terraform & scripts
│   ├── artifacts/                  # Screenshots & documentation
│   └── README.md                   # Complete project guide
├── 03-s3-static-website-terraform/  # Infrastructure as Code with Terraform
│   ├── provider.tf                 # LocalStack AWS provider configuration
│   ├── main.tf                     # Terraform resource definitions
│   ├── index.html                  # Website homepage
│   ├── error.html                  # Custom error page
│   └── README.md                   # Project documentation
├── 04-ec2-basics/                   # EC2 fundamentals with Python and Terraform
│   ├── python-version/              # Python/Boto3 implementation
│   │   ├── main.py                  # Complete EC2 workflow
│   │   ├── modules/                 # Reusable Python modules
│   │   ├── user_data/               # Bootstrap scripts
│   │   └── README.md                # Python version guide
│   ├── terraform-version/           # Terraform implementation
│   │   ├── main.tf                  # Terraform configuration
│   │   ├── modules/                 # Terraform modules
│   │   ├── user_data/               # Bootstrap scripts
│   │   └── README.md                # Terraform version guide
│   ├── docs/                        # EC2 documentation
│   └── README.md                    # Main project documentation
├── docs/                           # AWS certification materials
├── .env.example                    # Environment template
├── .gitignore                      # Git exclusions
└── README.md                       # This file
```

---

## Learning Path

### Phase 1: S3 Basics (Start Here!)
Perfect introduction to AWS cloud storage concepts.
- Create and manage S3 buckets
- Upload, download, and list files
- Understand endpoint URLs and credentials
- **Time**: 30 minutes
- **Navigate to**: [01-quickstart-s3](./01-quickstart-s3/)

### Phase 2: Serverless Architecture
Build a production-ready image processing application with AI style transfer.
- 4 Lambda functions (presign, list, resize, styletransfer)
- Event-driven S3 triggers
- Pre-signed URLs for secure uploads
- Google Gemini API integration for AI styling
- **Time**: 2-3 hours
- **Navigate to**: [02-serverless-image-resizer](./02-serverless-image-resizer/)

### Phase 3: Infrastructure as Code
Learn to provision AWS resources using Terraform with Infrastructure as Code principles.
- Terraform providers, variables, and outputs
- S3 static website hosting configuration
- Bucket policies and ACLs for public access
- Automated resource management with `tflocal`
- **Time**: 1 hour
- **Navigate to**: [03-s3-static-website-terraform](./03-s3-static-website-terraform/)

### Phase 4: EC2 Fundamentals
Master the core concepts of Amazon EC2 with both Python and Terraform implementations.
- Launch and manage virtual machines
- SSH key pairs and secure access
- Security groups and network configuration
- User data and cloud-init
- EBS volumes for persistent storage
- Instance lifecycle management
- Instance Metadata Service (IMDS)
- **Time**: 1-2 hours
- **Navigate to**: [04-ec2-basics](./04-ec2-basics/)

---

## Architecture Highlights

### Project 2: Serverless Image Resizer with AI

The crown jewel of this repository - a complete serverless application showcasing:

- **4 Lambda Functions**: presign, list, resize, styletransfer
- **4 S3 Buckets**: images, resized, styled, website
- **Event-Driven**: S3 triggers resize Lambda automatically
- **AI Integration**: Google Gemini API for artistic style transfer
- **Security**: Pre-signed URLs prevent credential exposure
- **Error Handling**: SNS/SES for failure notifications

![UI Screenshot](./02-serverless-image-resizer/artifacts/ui-three-columns.png)

*Three-column layout showing Original, Resized, and AI-styled images side-by-side*

### Project 3: Infrastructure as Code with Terraform

Your gateway to professional cloud engineering - learn to manage AWS resources through code:

- **Terraform Configuration**: Providers, variables, and state management
- **S3 Website Hosting**: Static website with custom error pages
- **Access Control**: Bucket policies and ACLs for public access
- **tflocal Integration**: LocalStack wrapper for seamless local development
- **Version Controlled**: Track infrastructure changes in git

### Project 4: EC2 Fundamentals

Your foundation in compute services - learn to launch and manage virtual machines:

- **Dual Implementation**: Python/Boto3 and Terraform versions for comprehensive learning
- **SSH Key Pairs**: Generate and manage secure access credentials
- **Security Groups**: Configure virtual firewalls with ingress rules
- **User Data**: Bootstrap instances with automated scripts
- **EBS Volumes**: Attach persistent storage to instances
- **Instance Metadata**: Query IMDS v1/v2 for self-configuration
- **Complete Lifecycle**: Launch, stop, start, and terminate instances
- **Documentation**: In-depth guides on EC2 concepts, networking, and troubleshooting

---

## Key AWS Concepts Covered

### Fundamental Services
- **S3**: Object storage, bucket policies, static website hosting
- **Lambda**: Serverless functions, event triggers, environment variables
- **EC2**: Virtual machines, key pairs, security groups, EBS volumes, user data
- **IAM**: Roles and permissions (using LocalStack's simplified model)

### Advanced Patterns
- **Serverless Architecture**: Stateless, event-driven computing
- **Pre-signed URLs**: Secure, temporary access without credentials
- **Dead Letter Queues (DLQ)**: Handling failed Lambda invocations
- **SSM Parameter Store**: Centralized configuration management
- **Infrastructure as Code (IaC)**: Terraform for reproducible deployments
- **VM Lifecycle Management**: Starting, stopping, and terminating instances

### Modern Integrations
- **AI/ML**: Google Gemini API for image style transfer
- **External APIs**: Handling API keys securely in serverless environments
- **Image Processing**: Pillow library in Lambda functions
- **Instance Metadata**: IMDS v1/v2 for instance self-configuration

---

## Common Commands

### LocalStack
```bash
localstack status              # Check if running
localstack logs               # View logs
localstack stop               # Stop LocalStack
```

### AWS CLI (via awslocal)
```bash
awslocal s3 ls                # List S3 buckets
awslocal lambda list-functions # List Lambda functions
awslocal ssm get-parameter --name /param/name  # Get parameter
```

### Project 2 Specific
```bash
cd 02-serverless-image-resizer/app
./deployment/build-lambdas.sh      # Build Lambda packages
./deployment/awslocal/deploy.sh    # Deploy all resources
```

---

## Documentation

- [LocalStack Documentation](https://docs.localstack.cloud/)
- [AWS Services Coverage](https://docs.localstack.cloud/aws/services/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

---

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](./CONTRIBUTING.md) and [Code of Conduct](./CODE_OF_CONDUCT.md) before submitting PRs.

---

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

## Acknowledgments

- **LocalStack Team** for the excellent AWS emulation platform
- **AWS Documentation** for comprehensive service guides
- **Google** for the Gemini API enabling AI features

---

**Happy Learning!** 🚀☁️

*Build, break, and rebuild AWS infrastructure safely with LocalStack.*

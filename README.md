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

---

## Prerequisites

### Required Software
- [Python 3.11+](https://www.python.org/downloads/)
- [UV Package Manager](https://docs.astral.sh/uv/)
- [Docker](https://www.docker.com/) (for Lambda functions)
- [LocalStack](https://docs.localstack.cloud/getting-started/)

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

---

## Key AWS Concepts Covered

### Fundamental Services
- **S3**: Object storage, bucket policies, static website hosting
- **Lambda**: Serverless functions, event triggers, environment variables
- **IAM**: Roles and permissions (using LocalStack's simplified model)

### Advanced Patterns
- **Serverless Architecture**: Stateless, event-driven computing
- **Pre-signed URLs**: Secure, temporary access without credentials
- **Dead Letter Queues (DLQ)**: Handling failed Lambda invocations
- **SSM Parameter Store**: Centralized configuration management
- **Infrastructure as Code (IaC)**: Terraform for reproducible deployments

### Modern Integrations
- **AI/ML**: Google Gemini API for image style transfer
- **External APIs**: Handling API keys securely in serverless environments
- **Image Processing**: Pillow library in Lambda functions

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

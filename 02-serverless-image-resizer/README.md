# Serverless Image Resizer with AI Style Transfer

> Complete serverless application: Image upload, resize, and AI-powered artistic transformation

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![LocalStack](https://img.shields.io/badge/LocalStack-AWS%20Emulation-blue)](https://localstack.cloud/)
[![Terraform](https://img.shields.io/badge/Terraform-IaC-623CE4?style=flat&logo=terraform)](https://www.terraform.io/)

Build a production-ready serverless image processing application with **AI style transfer** capabilities. This project demonstrates enterprise-grade AWS patterns using LocalStack for safe, local development.

**Based on**: [LocalStack Quickstart Guide](https://docs.localstack.cloud/aws/getting-started/quickstart/) | [Original Sample Repo](https://github.com/localstack-samples/sample-serverless-image-resizer-s3-lambda)

---

## Project Overview

This application provides a complete image processing pipeline:

✅ **Web Interface**: Upload images through a browser  
✅ **Pre-signed URLs**: Secure direct-to-S3 uploads (no credential exposure)  
✅ **Auto-Resize**: Lambda automatically resizes images to 400x400 pixels  
✅ **AI Style Transfer**: Google Gemini API applies artistic styles to images  
✅ **3-Column Display**: View Original, Resized, and AI-styled side-by-side  
✅ **Error Handling**: SNS/SES notifications for processing failures  
✅ **Infrastructure as Code**: Terraform deployment  

---

## User Interface

![Application UI](./artifacts/ui-three-columns.png)

*Three-column layout showing Original (1.9MB), Resized (14KB), and AI-styled (Anime style, 580KB) versions*

---

## Architecture

```
                         ┌─────────────────┐
                         │     User        │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   Web Browser   │
                         │ (S3 Static Site)│
                         └────────┬────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                             │
                    ▼                             ▼
         ┌─────────────────┐          ┌─────────────────┐
         │  Presign Lambda │          │  List Lambda    │
         │  (Generate URL) │          │ (Get all images)│
         └────────┬────────┘          └────────┬────────┘
                  │                              │
                  ▼                              │
         ┌─────────────────┐                     │
         │  S3 Images      │                     │
         │  (Original)     │─────────────────────┘
         └────────┬────────┘
                  │
                  │ S3 Event Trigger
                  ▼
         ┌─────────────────┐
         │  Resize Lambda  │──────────────────┐
         │  (400x400 max)  │                  │
         └────────┬────────┘                  │
                  │                         │ onFailure
                  ▼                         │
         ┌─────────────────┐                ▼
         │  S3 Resized     │      ┌─────────────────┐
         │  Bucket         │      │  SNS Topic      │
         └────────┬────────┘      │  (DLQ)          │
                  │               └────────┬────────┘
                  │                        │
     ┌────────────┴────────────┐            │
     │                         │            │
     ▼                         ▼            ▼
┌─────────┐            ┌──────────────┐   ┌──────┐
│ User    │            │  Styletransfer│   │ SES  │──────▶ Email
│ (Select │───────────▶│  Lambda       │   └──────┘
│ Style)  │   POST     │  (Gemini API) │
└─────────┘            └──────┬────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  S3 Styled      │
                       │  Bucket         │
                       └─────────────────┘
```

---

## AWS Services Used

| Service | Purpose | Count |
|---------|---------|-------|
| **S3** | Store original, resized, styled images + website | 4 buckets |
| **Lambda** | presign, list, resize, styletransfer | 4 functions |
| **SNS** | Dead Letter Queue for failure notifications | 1 topic |
| **SES** | Email notifications on failures | 1 service |
| **SSM Parameter Store** | Centralized configuration (bucket names) | 4 params |
| **CloudFront** | CDN distribution (Terraform) | 1 dist |

---

## Features

### AI Style Transfer (NEW!)

Apply artistic styles to your images using Google Gemini API:

| Style | Description |
|-------|-------------|
| 🎨 **Oil Painting** | Classic oil painting with visible brush strokes |
| 🌊 **Watercolor** | Soft watercolor painting with gentle washes |
| 🎌 **Anime** | Japanese anime style with vibrant colors |
| ✏️ **Sketch** | Detailed pencil sketch with fine lines |
| 🌻 **Van Gogh** | Impressionist style with bold colors |
| 🔮 **Cyberpunk** | Neon futuristic aesthetic |
| 📷 **Vintage** | Retro style with sepia tones |

### Web Interface Features

- **Upload Images**: Drag-and-drop or click to select
- **Automatic Resize**: 400x400 pixel thumbnails generated automatically
- **Style Selector**: Dropdown menu with all 7 AI styles
- **Apply Button**: One-click style transformation
- **Refresh Gallery**: Fetch all images with pre-signed URLs
- **Side-by-Side View**: Compare Original, Resized, and Styled versions

---

## Quick Start (5 minutes)

### Prerequisites

- [Python 3.11+](https://www.python.org/)
- [Docker](https://www.docker.com/) (for Lambda builds)
- [LocalStack](https://localstack.cloud/) with auth token
- [Google Gemini API Key](https://aistudio.google.com/app/apikey) (for AI features)

### 1. Clone and Setup

```bash
cd 02-serverless-image-resizer/app
```

### 2. Configure Environment

```bash
# Copy and edit the environment file
cp .env.example .env
# Edit .env and add:
# LOCALSTACK_AUTH_TOKEN=your_token
# GEMINI_API_KEY=your_gemini_api_key
```

### 3. Start LocalStack

```bash
# IMPORTANT: Must mount Docker socket for Lambda functions
docker run --rm -it -p 4566:4566 -p 4510-4559:4510-4559 \
  -e LOCALSTACK_AUTH_TOKEN=$LOCALSTACK_AUTH_TOKEN \
  -v /var/run/docker.sock:/var/run/docker.sock \
  localstack/localstack
```

### 4. Deploy with Terraform (Recommended)

```bash
cd deployment/terraform

terraform init
terraform apply -var="gemini_api_key=YOUR_API_KEY"
```

Or use the shell script deployment:

```bash
# Build Lambda packages (needs Docker)
./deployment/build-lambdas.sh

# Deploy resources
./deployment/awslocal/deploy.sh
```

### 5. Access the Application

```bash
# Get the website URL
awslocal s3api list-buckets --query "Buckets[?contains(Name, 'website')].Name" --output text

# Open in browser
http://localstack-website.s3-website.localhost.localstack.cloud:4566/
```

---

## Deployment Methods

### Method 1: Terraform (Infrastructure as Code)

**Recommended** for reproducible deployments and learning IaC concepts.

```bash
cd deployment/terraform

# Initialize Terraform
terraform init

# Plan the deployment
terraform plan -var="gemini_api_key=YOUR_API_KEY"

# Apply (deploy everything)
terraform apply -var="gemini_api_key=YOUR_API_KEY"

# Outputs will show Lambda URLs and website URL
```

**Variables** (in `variables.tf`):
- `gemini_api_key`: Your Google Gemini API key (required for styletransfer)
- `lambda_timeout`: Timeout for functions (default: 60s, styletransfer needs 120s)

### Method 2: Shell Scripts (Quick Start)

**Faster** for development and testing.

```bash
# From app/ directory
./deployment/build-lambdas.sh      # Build all Lambda packages
./deployment/awslocal/deploy.sh    # Deploy to LocalStack
```

**Note**: Shell script doesn't include AI style transfer. Use Terraform for full features.

---

## Lambda Functions

### 1. Presign Lambda

**Purpose**: Generate pre-signed POST URLs for secure S3 uploads

**Why Pre-signed URLs?**
- No AWS credentials in browser code
- Direct browser-to-S3 upload (bypasses Lambda)
- Temporary, expiring access
- Fine-grained permissions per upload

**Invocation**: HTTP GET → Returns JSON with upload URL and fields

### 2. List Lambda

**Purpose**: List all images from 3 buckets (original, resized, styled)

**Features**:
- Cross-bucket listing
- Generates pre-signed GET URLs for all images
- Returns structured JSON for frontend

**Invocation**: HTTP GET → Returns JSON array of all images with URLs

### 3. Resize Lambda

**Purpose**: Automatically resize uploaded images

**Trigger**: S3 Event (ObjectCreated on images bucket)

**Process**:
1. Download original from S3
2. Resize to 400x400 max using Pillow
3. Upload resized to resized bucket

**Timeout**: 60 seconds

### 4. Styletransfer Lambda (NEW!)

**Purpose**: Apply AI artistic styles using Google Gemini API

**Trigger**: HTTP POST (manual or via API Gateway)

**Process**:
1. Receive image key and style selection
2. Download from S3 Resized bucket
3. Base64 encode image
4. Call Gemini API with style-specific prompt
5. Decode base64 response image
6. Upload to S3 Styled bucket

**Timeout**: 120 seconds (Gemini API takes time)

**Styles Supported**: oil_painting, watercolor, anime, sketch, vangogh, cyberpunk, vintage

---

## Configuration

### Environment Variables (Lambda)

All Lambdas receive these via `STAGE=local` environment:

```python
# SSM Parameter Store paths used by functions
/localstack-thumbnail-app/buckets/images      # Original images
/localstack-thumbnail-app/buckets/resized     # Resized images  
/localstack-thumbnail-app/buckets/styled      # AI styled images
/localstack-thumbnail-app/buckets/website     # Static website
```

### SSM Parameter Store

Bucket names are stored as SSM parameters for centralized configuration:

```bash
# View parameters
awslocal ssm get-parameter \
  --name /localstack-thumbnail-app/buckets/images

# All parameters
awslocal ssm get-parameters-by-path \
  --path /localstack-thumbnail-app/buckets
```

---

## Testing

### Upload an Image

1. Open the website URL
2. Enter Lambda URLs (click "Load from API" button)
3. Drag-and-drop or select an image
4. Click Upload
5. Wait for upload to complete

### Apply AI Style

1. Click Refresh to see the uploaded image
2. Select a style from dropdown (e.g., "anime")
3. Click "Apply Style"
4. Wait 10-60 seconds (Gemini API processing)
5. Click Refresh to see all three versions

### Verify via CLI

```bash
# Check all buckets
awslocal s3 ls s3://localstack-thumbnails-app-images/
awslocal s3 ls s3://localstack-thumbnails-app-resized/
awslocal s3 ls s3://localstack-thumbnails-app-styled/

# Download styled image
awslocal s3 cp s3://localstack-thumbnails-app-styled/myimage.jpg ./

# Check Lambda logs
awslocal lambda get-function --function-name styletransfer
```

### Run Integration Tests

```bash
cd app
cd tests
pytest -v
```

Tests cover:
- Image resize functionality
- S3 event triggers
- SNS/SES failure notifications

---

## Development

### Project Structure

```
02-serverless-image-resizer/
├── app/
│   ├── lambdas/
│   │   ├── presign/              # Generate upload URLs
│   │   │   ├── handler.py
│   │   │   └── lambda.zip
│   │   ├── list/                 # List all images
│   │   │   ├── handler.py
│   │   │   └── lambda.zip
│   │   ├── resize/               # Auto-resize images
│   │   │   ├── handler.py
│   │   │   ├── requirements.txt  # Pillow==9.2.0
│   │   │   └── lambda.zip
│   │   └── styletransfer/        # AI style transfer
│   │       ├── handler.py
│   │       ├── requirements.txt  # boto3, requests
│   │       └── lambda.zip
│   ├── website/
│   │   ├── index.html            # Bootstrap 5 UI
│   │   ├── app.js                # jQuery frontend
│   │   └── favicon.ico
│   ├── deployment/
│   │   ├── terraform/
│   │   │   ├── main.tf           # Infrastructure as Code
│   │   │   ├── variables.tf      # Config variables
│   │   │   └── policies/         # IAM policies
│   │   ├── awslocal/
│   │   │   ├── deploy.sh         # Manual deployment
│   │   │   └── post-setup.sh     # S3 notifications
│   │   └── build-lambdas.sh      # Docker-based builds
│   ├── tests/
│   │   ├── test_integration.py   # pytest tests
│   │   └── nyan-cat.png          # Test image
│   └── .env.example              # Environment template
├── artifacts/
│   └── ui-three-columns.png      # Application screenshot
├── README.md                     # This file
└── DEPLOYMENT_COMPLETE.md        # Current deployment status
```

### Building Lambda Packages

**IMPORTANT**: Lambda packages must be built in Amazon Linux 2 environment for native dependencies (Pillow).

```bash
./deployment/build-lambdas.sh
```

This script:
1. Uses Docker with `public.ecr.aws/sam/build-python3.11` image
2. Installs requirements in Linux-compatible format
3. Creates `lambda.zip` packages
4. Includes all dependencies for each Lambda

### LocalStack Docker Notes

For Lambda functions to work, LocalStack MUST have Docker socket access:

```bash
docker run -v /var/run/docker.sock:/var/run/docker.sock ...
```

Without this, Lambda invocations will fail.

---

## Troubleshooting

### Lambda won't create
**Solution**: Check IAM role exists in Terraform policies

### S3 notification not triggering resize
**Solution**: 
- Verify Lambda ARN is correct in bucket notification
- Manually trigger: `awslocal lambda invoke --function-name resize --payload '{"Records": [...]}'`

### Resize Lambda fails
**Solution**: 
- Check Pillow is in lambda.zip (built with Docker)
- Lambda package must be built with Amazon Linux 2 image

### Website won't load
**Solution**: 
- Verify bucket has website config: `awslocal s3 website s3://bucket --index-document index.html`
- Check index.html exists in bucket

### Styletransfer Lambda timeout
**Solution**: 
- Increase timeout to 120 seconds (Gemini API takes 30-60s)
- Check GEMINI_API_KEY is set in Lambda environment
- Verify API key has Gemini API access

### Email notifications not working
**Solution**: 
- Check SNS subscription: `awslocal sns list-subscriptions-by-topic ...`
- View SES emails: `curl http://localhost.localstack.cloud:4566/_aws/ses`

---

## Key Concepts Learned

### Serverless Architecture Patterns
- **Event-driven**: S3 triggers Lambda automatically
- **Decoupled**: Each function has single responsibility
- **Stateless**: Functions don't maintain state between invocations
- **Serverless**: No servers to manage, pay-per-invocation model

### S3 Pre-signed URLs
- **Security**: Grant temporary access without credentials
- **Performance**: Client uploads directly to S3
- **Scalability**: No Lambda bottleneck for uploads
- **Flexibility**: Time-limited, IP-restricted, method-specific

### Dead Letter Queues (DLQ)
- **Reliability**: Failed events preserved for retry
- **Observability**: SNS/SES notify when failures occur
- **Debugging**: Inspect failed events in SNS topic

### Infrastructure as Code (IaC)
- **Reproducibility**: Same infrastructure every time
- **Version Control**: Track infrastructure changes in git
- **Collaboration**: Team members share infrastructure state
- **Safety**: Plan changes before applying

### AI Integration in Serverless
- **API Keys**: Secure storage in Lambda environment variables
- **Timeouts**: Long-running operations need higher timeout
- **Error Handling**: External API failures need graceful degradation
- **Base64 Encoding**: Image transmission via JSON APIs

---

## Next Steps

After mastering this project, consider:

### Extend the Application
- Add more AI styles (portrait, landscape, etc.)
- Implement image metadata extraction (EXIF)
- Add image format conversion (PNG ↔ JPG ↔ WebP)
- Create batch processing for multiple images

### Add More AWS Services
- **DynamoDB**: Store image metadata and user preferences
- **API Gateway**: Replace Lambda URLs with proper REST API
- **Cognito**: User authentication and authorization
- **Step Functions**: Orchestrate multi-step processing workflows
- **CloudWatch**: Monitoring, logging, and alarms

### Production Considerations
- Add input validation and sanitization
- Implement rate limiting
- Add image virus scanning
- Set up CloudFront caching
- Configure backup and disaster recovery

---

## Current Deployment Status

**Last Deployed**: See [DEPLOYMENT_COMPLETE.md](./DEPLOYMENT_COMPLETE.md) for current Lambda URLs and setup status.

**Active Lambda Functions**:
- presign: `http://...lambda-url.us-east-1.localhost.localstack.cloud:4566/`
- list: `http://...lambda-url.us-east-1.localhost.localstack.cloud:4566/`
- styletransfer: `http://...lambda-url.us-east-1.localhost.localstack.cloud:4566/`

**Website URL**: `http://localstack-website.s3-website.localhost.localstack.cloud:4566/`

---

## Resources

- [LocalStack Documentation](https://docs.localstack.cloud/)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/)
- [Google Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Pillow Documentation](https://pillow.readthedocs.io/)

---

**Happy Learning!** 🚀🎨☁️

*Build production-grade serverless applications with AI capabilities - all locally!*

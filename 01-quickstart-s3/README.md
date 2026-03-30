# 01-quickstart-s3

> S3 Fundamentals: Your first step into AWS cloud storage with LocalStack

This project teaches the foundational concepts of **Amazon S3** (Simple Storage Service) using LocalStack's AWS emulation. You'll create buckets, upload files, and learn how cloud storage works - all without AWS costs.

---

## What You'll Learn

By completing this project, you will understand:

✅ **S3 Buckets**: How to create and manage storage containers  
✅ **Object Storage**: Uploading, downloading, and listing files  
✅ **Boto3 Configuration**: Connecting Python to LocalStack's S3  
✅ **AWS Credentials**: Using test credentials with LocalStack  
✅ **Resource Cleanup**: Best practices for cleaning up resources  

---

## Prerequisites

1. **LocalStack must be running**
   ```bash
   localstack start
   ```

2. **Virtual environment activated**
   ```bash
   source ../.venv/bin/activate
   ```

3. **Python dependencies installed**
   ```bash
   uv sync
   ```

---

## Quick Start

```bash
python quickstart.py
```

This single command will:
1. Create a new S3 bucket
2. Upload sample files to it
3. List all files in the bucket
4. Download a file locally
5. Clean up by deleting all resources

---

## Key Concepts

### Endpoint URL

LocalStack provides all AWS services through a single endpoint:

```
http://localhost:4566
```

This is where S3, Lambda, and other services live in your local environment.

### AWS Credentials

LocalStack accepts any credentials. We use simple test values:

| Credential | Value | Purpose |
|------------|-------|---------|
| Access Key ID | `test` | LocalStack accepts any value |
| Secret Access Key | `test` | LocalStack accepts any value |
| Region | `us-east-1` | AWS region to use |

### Boto3 Client Configuration

```python
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1",
)
```

This creates an S3 client that talks to LocalStack instead of real AWS.

---

## What the Script Does

### Step-by-Step Breakdown

1. **Create Bucket** (`create_bucket`)
   - Creates a unique bucket name with timestamp
   - S3 bucket names must be globally unique (even in LocalStack)

2. **Upload Files** (`upload_file`)
   - Takes local files and stores them in S3
   - Files become "objects" with metadata

3. **List Contents** (`list_objects`)
   - Retrieves all objects from the bucket
   - Shows file names, sizes, and last modified dates

4. **Download Files** (`download_file`)
   - Retrieves objects from S3 to local filesystem
   - Demonstrates GET operations

5. **Cleanup** (`cleanup`)
   - Deletes all objects first (required before bucket deletion)
   - Deletes the empty bucket

---

## Code Structure

```
01-quickstart-s3/
├── quickstart.py              # Main learning script
└── README.md                  # This documentation
```

The `quickstart.py` file is organized into functions, each demonstrating a specific S3 operation. Read the code comments to understand what each function does.

---

## Common Operations Reference

### Using AWS CLI (awslocal)

```bash
# List all buckets
awslocal s3 ls

# Create a bucket
awslocal s3 mb s3://my-bucket-name

# Upload a file
awslocal s3 cp myfile.txt s3://my-bucket-name/

# Download a file
awslocal s3 cp s3://my-bucket-name/myfile.txt ./

# List bucket contents
awslocal s3 ls s3://my-bucket-name/

# Delete a file
awslocal s3 rm s3://my-bucket-name/myfile.txt

# Delete a bucket (must be empty first)
awslocal s3 rb s3://my-bucket-name

# Delete a bucket and all contents
awslocal s3 rb s3://my-bucket-name --force
```

### Using Boto3 (Python)

```python
# Create bucket
s3.create_bucket(Bucket="my-bucket")

# Upload file
s3.upload_file("local/path", "my-bucket", "s3-key")

# Download file
s3.download_file("my-bucket", "s3-key", "local/path")

# List objects
response = s3.list_objects_v2(Bucket="my-bucket")
for obj in response.get("Contents", []):
    print(obj["Key"])

# Delete object
s3.delete_object(Bucket="my-bucket", Key="s3-key")

# Delete bucket (must be empty)
s3.delete_bucket(Bucket="my-bucket")
```

---

## Troubleshooting

### Issue: Connection refused
**Solution**: LocalStack isn't running. Start it with:
```bash
localstack start
```

### Issue: Bucket already exists
**Solution**: Bucket names must be unique. The script adds timestamps to avoid this.

### Issue: Import errors
**Solution**: Activate the virtual environment:
```bash
source ../.venv/bin/activate
```

---

## Next Steps

After mastering S3 basics, try these exercises:

🔹 **Upload multiple files**: Modify the script to upload a directory  
🔹 **Create multiple buckets**: Practice bucket creation and management  
🔹 **Add metadata**: Include custom metadata when uploading files  
🔹 **Different regions**: Try creating buckets in different regions  
🔹 **Error handling**: Add try/except blocks to handle edge cases  

---

## Next Project

Ready for more? Move on to:

**[02-serverless-image-resizer](../02-serverless-image-resizer/)**

Learn Lambda functions, S3 event triggers, and build a complete serverless application with AI-powered image processing!

---

## Resources

- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [Boto3 S3 Reference](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)
- [LocalStack S3 Features](https://docs.localstack.cloud/aws/s3/)

---

**Happy Learning!** 📚☁️

*Start your AWS journey with the simplest yet most fundamental service.*

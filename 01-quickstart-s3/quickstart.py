"""
LocalStack Quickstart - S3 Basics
Following: https://docs.localstack.cloud/aws/getting-started/quickstart/

This script demonstrates:
1. Creating an S3 bucket
2. Uploading a file
3. Listing objects
4. Downloading a file
5. Cleaning up
"""

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# LocalStack endpoint
ENDPOINT_URL = "http://localhost:4566"
REGION = "us-east-1"

# AWS credentials for LocalStack (any values work)
AWS_ACCESS_KEY = "test"
AWS_SECRET_KEY = "test"


def get_s3_client():
    """Create S3 client pointing to LocalStack."""
    return boto3.client(
        "s3",
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=REGION,
    )


def create_bucket(bucket_name: str) -> bool:
    """Create an S3 bucket."""
    s3 = get_s3_client()
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"✅ Created bucket: {bucket_name}")
        return True
    except ClientError as e:
        print(f"❌ Error creating bucket: {e}")
        return False


def upload_file(bucket_name: str, file_path: str, object_name: str = None) -> bool:
    """Upload a file to S3 bucket."""
    if object_name is None:
        object_name = os.path.basename(file_path)

    s3 = get_s3_client()
    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"✅ Uploaded {file_path} to s3://{bucket_name}/{object_name}")
        return True
    except ClientError as e:
        print(f"❌ Error uploading file: {e}")
        return False


def list_objects(bucket_name: str) -> list:
    """List objects in an S3 bucket."""
    s3 = get_s3_client()
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        objects = response.get("Contents", [])
        print(f"\n📦 Objects in s3://{bucket_name}:")
        for obj in objects:
            print(f"  - {obj['Key']} ({obj['Size']} bytes)")
        return objects
    except ClientError as e:
        print(f"❌ Error listing objects: {e}")
        return []


def download_file(bucket_name: str, object_name: str, download_path: str) -> bool:
    """Download a file from S3 bucket."""
    s3 = get_s3_client()
    try:
        s3.download_file(bucket_name, object_name, download_path)
        print(f"✅ Downloaded s3://{bucket_name}/{object_name} to {download_path}")
        return True
    except ClientError as e:
        print(f"❌ Error downloading file: {e}")
        return False


def delete_bucket(bucket_name: str) -> bool:
    """Delete an S3 bucket and all its contents."""
    s3 = get_s3_client()
    try:
        # First, delete all objects
        response = s3.list_objects_v2(Bucket=bucket_name)
        objects = response.get("Contents", [])

        for obj in objects:
            s3.delete_object(Bucket=bucket_name, Key=obj["Key"])
            print(f"🗑️  Deleted s3://{bucket_name}/{obj['Key']}")

        # Then delete the bucket
        s3.delete_bucket(Bucket=bucket_name)
        print(f"✅ Deleted bucket: {bucket_name}")
        return True
    except ClientError as e:
        print(f"❌ Error deleting bucket: {e}")
        return False


def main():
    """Run the quickstart demo."""
    bucket_name = "my-test-bucket"
    test_file = "test-file.txt"
    download_path = "downloaded-file.txt"

    print("=" * 60)
    print("🚀 LocalStack S3 Quickstart Demo")
    print("=" * 60)

    # Create a test file
    with open(test_file, "w") as f:
        f.write("Hello from LocalStack!\nThis is a test file.")
    print(f"\n📝 Created test file: {test_file}")

    # Step 1: Create bucket
    print("\n" + "-" * 60)
    print("Step 1: Creating S3 bucket...")
    create_bucket(bucket_name)

    # Step 2: Upload file
    print("\n" + "-" * 60)
    print("Step 2: Uploading file...")
    upload_file(bucket_name, test_file)

    # Step 3: List objects
    print("\n" + "-" * 60)
    print("Step 3: Listing objects...")
    list_objects(bucket_name)

    # Step 4: Download file
    print("\n" + "-" * 60)
    print("Step 4: Downloading file...")
    download_file(bucket_name, test_file, download_path)

    # Verify download
    with open(download_path, "r") as f:
        content = f.read()
    print(f"\n📄 Downloaded content:\n{content}")

    # Step 5: Cleanup
    print("\n" + "-" * 60)
    print("Step 5: Cleaning up...")
    delete_bucket(bucket_name)

    # Remove local files
    os.remove(test_file)
    os.remove(download_path)
    print(f"🗑️  Removed local files: {test_file}, {download_path}")

    print("\n" + "=" * 60)
    print("✨ Demo completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()

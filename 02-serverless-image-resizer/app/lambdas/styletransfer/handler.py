import base64
import json
import os
import typing
import uuid
from io import BytesIO
from urllib.parse import unquote_plus

import boto3
import requests

if typing.TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_ssm import SSMClient

endpoint_url = None
if os.getenv("STAGE") == "local":
    endpoint_url = "https://localhost.localstack.cloud:4566"

s3: "S3Client" = boto3.client("s3", endpoint_url=endpoint_url)
ssm: "SSMClient" = boto3.client("ssm", endpoint_url=endpoint_url)

# Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent"

# Style prompts mapping
STYLE_PROMPTS = {
    "oil_painting": "Transform this image into a classic oil painting with visible brush strokes, rich colors, and artistic texture",
    "watercolor": "Convert this image into a soft watercolor painting with gentle washes, flowing colors, and artistic transparency",
    "anime": "Transform this image into Japanese anime style with vibrant colors, clean lines, and characteristic anime aesthetics",
    "sketch": "Convert this image into a detailed pencil sketch with fine lines, shading, and hand-drawn appearance",
    "vangogh": "Transform this image into Van Gogh style with swirling brush strokes, bold colors, and impressionist texture",
    "cyberpunk": "Convert this image into cyberpunk style with neon lights, futuristic atmosphere, and high-tech urban aesthetic",
    "vintage": "Transform this image into vintage retro style with sepia tones, film grain, and nostalgic atmosphere",
}


def get_bucket_names() -> tuple:
    """Get source and styled bucket names from SSM."""
    images_param = ssm.get_parameter(Name="/localstack-thumbnail-app/buckets/images")
    styled_param = ssm.get_parameter(Name="/localstack-thumbnail-app/buckets/styled")
    return (images_param["Parameter"]["Value"], styled_param["Parameter"]["Value"])


def download_image(bucket: str, key: str) -> bytes:
    """Download image from S3 and return as bytes."""
    response = s3.get_object(Bucket=bucket, Key=key)
    return response["Body"].read()


def upload_styled_image(bucket: str, key: str, image_data: bytes) -> int:
    """Upload styled image to S3 and return size."""
    s3.put_object(Bucket=bucket, Key=key, Body=image_data, ContentType="image/png")
    # Get the size of uploaded object
    response = s3.head_object(Bucket=bucket, Key=key)
    return response["ContentLength"]


def call_gemini_api(image_data: bytes, style: str) -> bytes:
    """Call Gemini API to apply style transfer.

    Returns styled image as bytes.
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    if style not in STYLE_PROMPTS:
        raise ValueError(
            f"Unknown style: {style}. Available: {list(STYLE_PROMPTS.keys())}"
        )

    # Encode image to base64
    image_b64 = base64.b64encode(image_data).decode("utf-8")

    # Build the request
    url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"

    prompt = STYLE_PROMPTS[style]

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"{prompt}. Return the styled image as the response."},
                    {"inline_data": {"mime_type": "image/png", "data": image_b64}},
                ]
            }
        ],
        "generationConfig": {"responseModalities": ["Text", "Image"]},
    }

    headers = {"Content-Type": "application/json"}

    # Call Gemini API
    response = requests.post(url, json=payload, headers=headers, timeout=60)

    if response.status_code != 200:
        raise Exception(f"Gemini API error: {response.status_code} - {response.text}")

    result = response.json()

    # Extract image from response
    # Gemini returns image in parts array
    if "candidates" in result and len(result["candidates"]) > 0:
        candidate = result["candidates"][0]
        if "content" in candidate and "parts" in candidate["content"]:
            for part in candidate["content"]["parts"]:
                if "inlineData" in part:
                    # Found the image
                    image_b64_response = part["inlineData"]["data"]
                    return base64.b64decode(image_b64_response)

    raise Exception("No image returned from Gemini API")


def handler(event, context):
    """Main Lambda handler for style transfer."""
    try:
        # Parse request
        path = event.get("rawPath", "").lstrip("/")
        if not path:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Image key required in path"}),
            }

        key = unquote_plus(path)

        # Parse body for style
        body = event.get("body", "{}")
        if isinstance(body, str):
            body = json.loads(body)

        style = body.get("style", "")
        if not style:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Style parameter required"}),
            }

        # Get bucket names
        source_bucket, styled_bucket = get_bucket_names()

        # Download original image
        print(f"Downloading {key} from {source_bucket}")
        image_data = download_image(source_bucket, key)

        # Call Gemini API
        print(f"Applying style: {style}")
        styled_image_data = call_gemini_api(image_data, style)

        # Upload to styled bucket
        print(f"Uploading styled image to {styled_bucket}/{key}")
        styled_size = upload_styled_image(styled_bucket, key, styled_image_data)

        # Generate presigned URL for the styled image
        styled_url = s3.generate_presigned_url(
            "get_object", Params={"Bucket": styled_bucket, "Key": key}, ExpiresIn=3600
        )

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {
                    "success": True,
                    "message": f"Style '{style}' applied successfully",
                    "image_key": key,
                    "style": style,
                    "styled_size": styled_size,
                    "styled_url": styled_url,
                }
            ),
        }

    except ValueError as e:
        print(f"Validation error: {str(e)}")
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)}),
        }
    except Exception as e:
        print(f"Error during style transfer: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": f"Style transfer failed: {str(e)}"}),
        }

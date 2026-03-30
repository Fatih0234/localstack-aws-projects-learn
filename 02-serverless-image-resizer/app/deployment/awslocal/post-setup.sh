#!/bin/bash
# Post-deployment setup script
# Run this after the main deployment to set up S3 notifications

export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT_URL=http://localhost:4566

echo "🔧 Setting up S3 bucket notifications..."

# Add permission for S3 to invoke resize Lambda
aws --endpoint-url=$AWS_ENDPOINT_URL lambda add-permission \
  --function-name resize \
  --statement-id s3-invoke-resize \
  --action lambda:InvokeFunction \
  --principal s3.amazonaws.com \
  --source-arn arn:aws:s3:::localstack-thumbnails-app-images 2>/dev/null || true

# Setup bucket notification
aws --endpoint-url=$AWS_ENDPOINT_URL s3api put-bucket-notification-configuration \
  --bucket localstack-thumbnails-app-images \
  --notification-configuration '{
    "LambdaFunctionConfigurations": [{
      "Id": "resize-trigger",
      "LambdaFunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:resize",
      "Events": ["s3:ObjectCreated:*"]
    }]
  }' 2>/dev/null || echo "⚠️  S3 notification setup failed - you may need to manually trigger resize"

echo "✅ Setup complete!"

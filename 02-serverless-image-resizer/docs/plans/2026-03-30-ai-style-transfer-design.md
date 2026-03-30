# AI Style Transfer Feature Design

**Date:** 2026-03-30  
**Project:** 02-serverless-image-resizer  
**Feature:** Async AI Style Transfer using Gemini API

## Overview

Add AI-powered style transfer capability to the existing serverless image resizer. Users can upload images (which get resized automatically), then apply artistic styles using Google's Gemini API.

## Architecture

### New Components

1. **New S3 Bucket**: `localstack-thumbnails-app-styled`
   - Stores AI-generated styled images
   - Same structure as resized bucket

2. **New Lambda Function**: `styletransfer`
   - Location: `/app/lambdas/styletransfer/`
   - Triggered: By HTTP API (not S3 event)
   - Flow:
     - Receives request: `{image_key: "photo.jpg", style: "oil_painting"}`
     - Downloads original from S3
     - Calls Gemini API with image + style prompt
     - Receives styled image (base64 or URL)
     - Uploads result to styled bucket
     - Returns styled image metadata

3. **Modified Components**:
   - **List Lambda**: Query 3 buckets (original, resized, styled)
   - **Frontend**: Add style selector + "Apply Style" button per image
   - **SSM Parameter**: Add `/localstack-thumbnail-app/buckets/styled`

### Data Model

```json
{
  "Name": "photo.jpg",
  "Timestamp": "2024-01-15T10:30:00+00:00",
  "Original": {
    "Size": 2456789,
    "URL": "https://.../photo.jpg?..."
  },
  "Resized": {
    "Size": 45234,
    "URL": "https://.../photo.jpg?..."
  },
  "Styled": {
    "Size": 89123,
    "URL": "https://.../photo.jpg?...",
    "Style": "oil_painting",
    "Prompt": "Transform this image into an oil painting style"
  }
}
```

### Style Options

Available styles in dropdown:
1. **oil_painting** - Classic oil painting look
2. **watercolor** - Soft watercolor effect  
3. **anime** - Japanese anime/cartoon style
4. **sketch** - Pencil sketch drawing
5. **vangogh** - Van Gogh impressionist style
6. **cyberpunk** - Neon cyberpunk aesthetic
7. **vintage** - Retro/vintage photo look

### API Flow

**Style Transfer Request:**
```
POST /{image_key}
Content-Type: application/json

{
  "style": "oil_painting"
}
```

**Response:**
```json
{
  "statusCode": 200,
  "body": {
    "success": true,
    "message": "Style transfer initiated",
    "image_key": "photo.jpg",
    "style": "oil_painting",
    "styled_url": "https://.../styled/photo.jpg?..."
  }
}
```

### Frontend Changes

1. **Image Card Template** - Add:
   - Style selector dropdown (when no styled version exists)
   - "Apply Style" button
   - Third image display section (styled version)
   - Style badge showing which style was applied

2. **Style Transfer Flow**:
   - User selects style from dropdown
   - Clicks "Apply Style" button
   - Frontend shows loading spinner
   - Calls styletransfer Lambda
   - On success: Refreshes image list to show styled version
   - Styled image appears alongside original and resized

### Security Considerations

- Gemini API key stored in `.env` file (not committed)
- Lambda environment variable: `GEMINI_API_KEY`
- Rate limiting on styletransfer Lambda (prevent API abuse)
- API key validation before calling Gemini

### Error Handling

**Gemini API Errors:**
- Timeout: Return 504, styled image won't be created
- Rate limit: Return 429 with retry-after header
- Invalid image: Return 400 with error message
- API failure: Log to CloudWatch, SNS notification optional

**S3 Errors:**
- Image not found: Return 404
- Upload failure: Retry logic with exponential backoff

### Implementation Steps

1. Create S3 bucket for styled images
2. Create styletransfer Lambda function
3. Update List Lambda to query styled bucket
4. Add SSM parameter for styled bucket name
5. Update Terraform to deploy new resources
6. Update frontend HTML/JS
7. Test end-to-end flow

## Success Criteria

- [ ] User can upload image and get it resized (existing functionality)
- [ ] User can select a style and apply it to any uploaded image
- [ ] Styled image appears in the UI alongside original and resized
- [ ] List Lambda returns all 3 versions (original, resized, styled)
- [ ] API key is securely stored in environment variable
- [ ] Error handling works for failed style transfers

## Technical Decisions

1. **Why HTTP trigger instead of S3 event?**
   - Gives user control over when to apply style
   - Prevents accidental API costs from bulk uploads
   - Allows user to preview resized image first

2. **Why separate styled bucket?**
   - Consistent with existing architecture pattern
   - Easy to manage lifecycle policies per output type
   - Clean separation of concerns

3. **Why use Gemini API instead of local model?**
   - Solves Lambda 50MB size limit issue
   - No need to package ML libraries
   - Better quality than simple filter-based styles
   - Google's models are well-maintained

## Future Enhancements

- [ ] Batch style transfer (multiple images at once)
- [ ] Style preview before applying
- [ ] Custom prompt input (advanced mode)
- [ ] Style history/versioning
- [ ] Download all variants as ZIP

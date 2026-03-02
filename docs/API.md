# Smart Vendors API Documentation

## Overview

The Smart Vendors API is a serverless REST API built on AWS Lambda and API Gateway. All endpoints return JSON responses and use standard HTTP status codes.

**Base URL**: `https://[API_ID].execute-api.[REGION].amazonaws.com/prod`

**Authentication**: API Key (passed in `x-api-key` header) or IAM authentication for production. Demo mode uses open access.

## Table of Contents

- [Voice & Transactions](#voice--transactions)
- [Market Prices](#market-prices)
- [Freshness Classification](#freshness-classification)
- [Marketplace](#marketplace)
- [Trust Score](#trust-score)
- [Error Responses](#error-responses)

---

## Voice & Transactions

### POST /voice/transcribe

Transcribe audio to text and extract transaction details using AWS Transcribe and Bedrock.

**Request Body**:
```json
{
  "audio": "base64_encoded_audio_data",
  "language_code": "hi-IN",
  "vendor_id": "vendor-uuid",
  "media_format": "mp3"
}
```

**Parameters**:
- `audio` (string, required): Base64-encoded audio file
- `language_code` (string, optional): Language code. Supported: `hi-IN` (Hindi), `en-IN` (English). Default: `en-IN`
- `vendor_id` (string, required): Vendor UUID
- `media_format` (string, optional): Audio format (`mp3`, `wav`, `ogg`). Default: `mp3`

**Response** (200 OK):
```json
{
  "transcription": {
    "text": "Do kilo tamatar pachas rupaye",
    "confidence": 0.95,
    "language": "hi-IN"
  },
  "extracted_transaction": {
    "item_name": "tomatoes",
    "quantity": 2.0,
    "unit": "kg",
    "price_per_unit": 25.0,
    "total_amount": 50.0,
    "extracted_successfully": true
  }
}
```

**Error Responses**:
- `400 Bad Request`: Missing required parameters or unsupported language
- `500 Internal Server Error`: Transcription or extraction failed

**Example**:
```bash
curl -X POST https://api.example.com/voice/transcribe \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "audio": "SGVsbG8gV29ybGQ=",
    "language_code": "hi-IN",
    "vendor_id": "demo-vendor-001"
  }'
```

---

### POST /transactions

Create a transaction from transcribed text using Bedrock NLP.

**Request Body**:
```json
{
  "text": "Sold 2 kg tomatoes for 50 rupees",
  "vendor_id": "vendor-uuid",
  "language_code": "en-IN"
}
```

**Parameters**:
- `text` (string, required): Transcribed text or manual input
- `vendor_id` (string, required): Vendor UUID
- `language_code` (string, optional): Language code. Default: `en-IN`

**Response** (201 Created):
```json
{
  "transaction_id": "txn-uuid",
  "vendor_id": "vendor-uuid",
  "item_name": "tomatoes",
  "quantity": 2.0,
  "unit": "kg",
  "price_per_unit": 25.0,
  "total_amount": 50.0,
  "extracted_successfully": true
}
```

**Error Responses**:
- `400 Bad Request`: Missing required parameters
- `500 Internal Server Error`: Transaction creation failed

---

### GET /transactions/{vendor_id}

Retrieve transaction history for a vendor.

**Path Parameters**:
- `vendor_id` (string, required): Vendor UUID

**Query Parameters**:
- `limit` (integer, optional): Maximum number of transactions to return. Default: 20
- `start_date` (string, optional): ISO 8601 date to filter from
- `end_date` (string, optional): ISO 8601 date to filter to

**Response** (200 OK):
```json
{
  "vendor_id": "vendor-uuid",
  "transactions": [
    {
      "transaction_id": "txn-uuid-1",
      "item_name": "tomatoes",
      "quantity": 2.0,
      "unit": "kg",
      "price_per_unit": 25.0,
      "total_amount": 50.0,
      "timestamp": "2024-01-15T10:30:00Z",
      "recorded_via": "voice"
    },
    {
      "transaction_id": "txn-uuid-2",
      "item_name": "potatoes",
      "quantity": 5.0,
      "unit": "kg",
      "price_per_unit": 20.0,
      "total_amount": 100.0,
      "timestamp": "2024-01-15T11:45:00Z",
      "recorded_via": "manual"
    }
  ],
  "count": 2,
  "total_amount": 150.0
}
```

**Example**:
```bash
curl -X GET "https://api.example.com/transactions/demo-vendor-001?limit=10" \
  -H "x-api-key: YOUR_API_KEY"
```

---

## Market Prices

### GET /prices/{item}

Get market prices from multiple mandis for a produce item.

**Path Parameters**:
- `item` (string, required): Produce item name (e.g., `tomatoes`, `potatoes`, `onions`)

**Query Parameters**:
- `limit` (integer, optional): Number of mandis to return. Default: 3

**Response** (200 OK):
```json
{
  "item": "tomatoes",
  "prices": [
    {
      "item_name": "tomatoes",
      "mandi_name": "Azadpur Mandi",
      "price_per_kg": 25.0,
      "distance_km": 5.2,
      "timestamp": "2024-01-15T06:00:00Z"
    },
    {
      "item_name": "tomatoes",
      "mandi_name": "Ghazipur Mandi",
      "price_per_kg": 28.0,
      "distance_km": 12.5,
      "timestamp": "2024-01-15T06:00:00Z"
    },
    {
      "item_name": "tomatoes",
      "mandi_name": "Okhla Mandi",
      "price_per_kg": 26.5,
      "distance_km": 8.3,
      "timestamp": "2024-01-15T06:00:00Z"
    }
  ],
  "count": 3
}
```

**Error Responses**:
- `400 Bad Request`: Missing item parameter
- `404 Not Found`: No prices found for item
- `500 Internal Server Error`: Price query failed

**Example**:
```bash
curl -X GET https://api.example.com/prices/tomatoes \
  -H "x-api-key: YOUR_API_KEY"
```

---

## Freshness Classification

### POST /freshness/classify

Classify produce freshness using SageMaker ML model.

**Request Body**:
```json
{
  "image": "base64_encoded_image_data",
  "vendor_id": "vendor-uuid"
}
```

**Parameters**:
- `image` (string, required): Base64-encoded image file (JPEG, PNG)
- `vendor_id` (string, required): Vendor UUID

**Response** (200 OK):
```json
{
  "category": "Fresh",
  "confidence": 0.92,
  "shelf_life_hours": 48,
  "suggestions": [
    "Store in cool, dry place",
    "Sell within 2 days for best quality"
  ]
}
```

**Categories**:
- `Fresh`: High quality, ready for sale (confidence > 0.7)
- `B-Grade`: Slightly aged, suitable for juice/processing (confidence 0.4-0.7)
- `Waste`: Not suitable for sale, compost recommended (confidence < 0.4)

**Error Responses**:
- `400 Bad Request`: Missing required parameters or invalid image
- `500 Internal Server Error`: Classification failed

**Example**:
```bash
curl -X POST https://api.example.com/freshness/classify \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "image": "/9j/4AAQSkZJRgABAQEAYABgAAD...",
    "vendor_id": "demo-vendor-001"
  }'
```

---

## Marketplace

### POST /marketplace/listings

Create a B-Grade produce listing on the marketplace.

**Request Body**:
```json
{
  "vendor_id": "vendor-uuid",
  "item_name": "tomatoes",
  "weight_kg": 10.0,
  "price": 150.0,
  "condition": "B-Grade"
}
```

**Parameters**:
- `vendor_id` (string, required): Vendor UUID
- `item_name` (string, required): Produce item name
- `weight_kg` (number, required): Weight in kilograms
- `price` (number, required): Total price in rupees
- `condition` (string, optional): Condition. Default: `B-Grade`

**Response** (201 Created):
```json
{
  "listing_id": "listing-uuid",
  "vendor_id": "vendor-uuid",
  "item_name": "tomatoes",
  "weight_kg": 10.0,
  "price": 150.0,
  "condition": "B-Grade",
  "status": "active",
  "buyers_notified": 5,
  "mandi_credits_earned": 100,
  "created_at": "2024-01-15T14:30:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Missing required parameters or invalid values
- `500 Internal Server Error`: Listing creation failed

---

### GET /marketplace/buyers

Find nearby buyers for B-Grade produce.

**Query Parameters**:
- `item` (string, required): Produce item name
- `latitude` (number, required): Vendor latitude
- `longitude` (number, required): Vendor longitude
- `radius_km` (number, optional): Search radius in km. Default: 10

**Response** (200 OK):
```json
{
  "buyers": [
    {
      "buyer_id": "buyer-uuid-1",
      "name": "Juice Corner",
      "type": "juice_shop",
      "distance_km": 2.5,
      "interested_items": ["tomatoes", "oranges"],
      "phone": "+91-98765-43210"
    },
    {
      "buyer_id": "buyer-uuid-2",
      "name": "Pickle Factory",
      "type": "processing_unit",
      "distance_km": 5.8,
      "interested_items": ["tomatoes", "mangoes"],
      "phone": "+91-98765-43211"
    }
  ],
  "count": 2
}
```

---

### POST /marketplace/notify

Notify buyers about a new listing (simulated for demo).

**Request Body**:
```json
{
  "listing_id": "listing-uuid",
  "buyer_ids": ["buyer-uuid-1", "buyer-uuid-2"]
}
```

**Response** (200 OK):
```json
{
  "listing_id": "listing-uuid",
  "notifications_sent": 2,
  "status": "success"
}
```

---

## Trust Score

### GET /trust-score/{vendor_id}

Get Trust Score and tier for a vendor.

**Path Parameters**:
- `vendor_id` (string, required): Vendor UUID

**Response** (200 OK):
```json
{
  "vendor_id": "vendor-uuid",
  "trust_score": 150,
  "tier": "Silver",
  "next_tier": "Gold",
  "points_to_next_tier": 100,
  "breakdown": {
    "transactions": 120,
    "marketplace_sales": 20,
    "price_reports": 10
  },
  "tier_benefits": [
    "Priority buyer matching",
    "Lower marketplace fees",
    "Credit pre-approval"
  ]
}
```

**Tier Thresholds**:
- Bronze: 0-99 points
- Silver: 100-249 points
- Gold: 250+ points

**Example**:
```bash
curl -X GET https://api.example.com/trust-score/demo-vendor-001 \
  -H "x-api-key: YOUR_API_KEY"
```

---

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error message describing what went wrong"
}
```

### HTTP Status Codes

- `200 OK`: Request succeeded
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid API key
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

### Common Error Messages

- `"Missing audio data"`: Audio parameter not provided in request
- `"Unsupported language: xx-XX"`: Language code not supported
- `"Missing vendor_id"`: Vendor ID not provided
- `"Failed to process voice transaction"`: Transcription or extraction failed
- `"Internal server error"`: Unexpected server error (check CloudWatch logs)

---

## Rate Limits

**Demo Mode**: No rate limits

**Production**: 
- 100 requests per minute per API key
- 1000 requests per hour per API key

Rate limit headers included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642252800
```

---

## Demo Credentials

For testing the API, use these demo credentials:

**Vendor ID**: `demo-vendor-001`

**API Key**: Contact team for demo API key or use IAM authentication

---

## AWS Services Integration

The API leverages these AWS services:

- **AWS Lambda**: Serverless compute for all endpoints
- **Amazon API Gateway**: HTTP API routing and management
- **AWS Transcribe**: Speech-to-text for voice input
- **Amazon Bedrock**: NLP for transaction extraction
- **Amazon SageMaker**: ML inference for freshness classification
- **Amazon DynamoDB**: NoSQL database for all data storage
- **Amazon S3**: Storage for audio files and images
- **Amazon SNS**: Buyer notifications

---

## Support

For API issues or questions:
- Email: your-email@example.com
- GitHub Issues: https://github.com/your-username/smart-vendors/issues
- Documentation: https://github.com/your-username/smart-vendors/tree/main/docs

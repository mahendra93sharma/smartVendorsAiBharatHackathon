# Smart Vendors API - Bruno Collection

This Bruno collection contains all the API endpoints for the Smart Vendors platform.

## Setup Instructions

1. **Install Bruno**: Download from [usebruno.com](https://www.usebruno.com/)

2. **Import Collection**: 
   - Open Bruno
   - Click "Open Collection"
   - Navigate to the `bruno-collection` folder
   - Select the folder to import

3. **Configure Environment**:
   - Select the environment (Local or Production) from the dropdown
   - Update the variables in the environment file:
     - `base_url`: Your API Gateway URL
     - `api_key`: Your API key (if required)
     - `vendor_id`: Your vendor ID

## Environments

### Local
- Base URL: `http://localhost:8000`
- For local development and testing

### Production
- Base URL: `https://your-api-id.execute-api.ap-south-1.amazonaws.com/prod`
- For production AWS deployment
- **Update the `base_url` with your actual API Gateway URL**

## API Endpoints

### Voice & Transactions
1. **Voice Transcribe** - POST `/voice/transcribe`
   - Transcribe audio and extract transaction details
   - Supports Hindi (hi-IN) and English (en-IN)

2. **Create Transaction** - POST `/transactions`
   - Create transaction from text input

3. **Get Transactions** - GET `/transactions/{vendor_id}`
   - Retrieve transaction history

### Market Prices
4. **Get Market Prices** - GET `/prices/{item}`
   - Get prices from multiple mandis

### Freshness Classification
5. **Classify Freshness** - POST `/freshness/classify`
   - Classify produce freshness using ML

### Marketplace
6. **Create Marketplace Listing** - POST `/marketplace/listings`
   - Create B-Grade produce listing

7. **Get Marketplace Buyers** - GET `/marketplace/buyers`
   - Find nearby buyers

8. **Notify Marketplace Buyers** - POST `/marketplace/notify`
   - Notify buyers about listing

### Trust Score
9. **Get Trust Score** - GET `/trust-score/{vendor_id}`
   - Get vendor trust score and tier

## Authentication

All endpoints require an API key passed in the `x-api-key` header. The key is automatically included from the environment variables.

## Testing Tips

1. **Voice Transcribe**: Use a base64-encoded audio file. You can use online tools to convert audio to base64.

2. **Classify Freshness**: Use a base64-encoded image. Test with produce images.

3. **Demo Vendor ID**: Use `demo-vendor-001` for testing.

## Common Issues

### CORS Errors
If you get CORS errors when testing from the browser, make sure your API Gateway has CORS enabled.

### Authentication Errors
Verify your API key is correct in the environment variables.

### Base64 Encoding
For audio and image endpoints, ensure your base64 data doesn't include the data URI prefix (e.g., `data:image/jpeg;base64,`). Only include the base64 string.

## Support

For API documentation, see `docs/API.md` in the project root.

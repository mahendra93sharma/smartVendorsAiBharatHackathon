# Smart Vendors Frontend - AWS API Integration Guide

## ✅ API Integration Complete!

Your frontend is now configured to use the deployed AWS API Gateway backend.

---

## 🌐 API Configuration

### Current Setup

**API Base URL**: `https://ji5ymmu4g7.execute-api.ap-south-1.amazonaws.com`

This URL is configured in:
- `frontend/.env` - Active configuration
- `frontend/.env.example` - Template for others
- `frontend/src/config/api.ts` - TypeScript configuration

### Environment Variables

```env
# Production AWS API Gateway
VITE_API_BASE_URL=https://ji5ymmu4g7.execute-api.ap-south-1.amazonaws.com
VITE_API_GATEWAY_URL=https://ji5ymmu4g7.execute-api.ap-south-1.amazonaws.com

# AWS Region
VITE_AWS_REGION=ap-south-1

# Feature Flags
VITE_ENABLE_DEMO_MODE=true
VITE_ENABLE_OFFLINE_MODE=true
```

---

## 📡 Available API Endpoints

All endpoints are now accessible through your frontend:

### 1. Voice Transcription
```typescript
POST /voice/transcribe
{
  "audio": "base64_encoded_audio",
  "vendor_id": "vendor-123",
  "language_code": "hi-IN"
}
```

### 2. Transaction Management
```typescript
// Create transaction
POST /transactions
{
  "text": "2 kg tomatoes 50 rupees",
  "vendor_id": "vendor-123",
  "language_code": "en-IN"
}

// Get transactions
GET /transactions/{vendor_id}
```

### 3. Market Prices
```typescript
GET /prices/{item}
// Example: /prices/tomatoes
```

### 4. Freshness Classification
```typescript
POST /freshness/classify
{
  "image": "base64_encoded_image",
  "vendor_id": "vendor-123"
}
```

### 5. Marketplace
```typescript
// Create listing
POST /marketplace/listings
{
  "vendor_id": "vendor-123",
  "item_name": "tomatoes",
  "weight_kg": 10.0,
  "price": 200.0
}

// Get buyers
GET /marketplace/buyers

// Notify buyers
POST /marketplace/notify
{
  "listing_id": "listing-123"
}
```

### 6. Trust Score
```typescript
GET /trust-score/{vendor_id}
// Example: /trust-score/vendor-123
```

---

## 🔧 How to Use in Your Components

### Using the API Service

The frontend already has an API service configured. Here's how to use it:

```typescript
import { apiService } from '../services/api'

// Example: Get market prices
const prices = await apiService.get('/prices/tomatoes')

// Example: Create transaction
const transaction = await apiService.post('/transactions', {
  text: "2 kg tomatoes 50 rupees",
  vendor_id: "vendor-123",
  language_code: "en-IN"
})

// Example: Get vendor transactions
const transactions = await apiService.get(`/transactions/${vendorId}`)

// Example: Upload image for freshness classification
const result = await apiService.post('/freshness/classify', {
  image: base64Image,
  vendor_id: vendorId
})
```

### Example Component

```typescript
import { useState, useEffect } from 'react'
import { apiService } from '../services/api'

function MarketPrices() {
  const [prices, setPrices] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchPrices() {
      try {
        const data = await apiService.get('/prices/tomatoes')
        setPrices(data.prices)
      } catch (error) {
        console.error('Failed to fetch prices:', error)
      } finally {
        setLoading(false)
      }
    }
    
    fetchPrices()
  }, [])

  if (loading) return <div>Loading...</div>

  return (
    <div>
      <h2>Market Prices</h2>
      {prices.map(price => (
        <div key={price.mandi_name}>
          {price.mandi_name}: ₹{price.price_per_kg}/kg
        </div>
      ))}
    </div>
  )
}
```

---

## 🧪 Testing the Integration

### 1. Start the Frontend

```bash
cd frontend
npm run dev
```

The frontend will now use the AWS API Gateway for all API calls.

### 2. Test API Calls

Open your browser console and test:

```javascript
// Test market prices
fetch('https://ji5ymmu4g7.execute-api.ap-south-1.amazonaws.com/prices/tomatoes')
  .then(r => r.json())
  .then(console.log)

// Test transactions
fetch('https://ji5ymmu4g7.execute-api.ap-south-1.amazonaws.com/transactions/vendor-123')
  .then(r => r.json())
  .then(console.log)
```

### 3. Check Network Tab

1. Open browser DevTools (F12)
2. Go to Network tab
3. Interact with your app
4. Verify requests go to `ji5ymmu4g7.execute-api.ap-south-1.amazonaws.com`

---

## 🔄 Switching Between Environments

### Use Production API (Current)
```env
VITE_API_BASE_URL=https://ji5ymmu4g7.execute-api.ap-south-1.amazonaws.com
```

### Use Local Development
```env
VITE_API_BASE_URL=http://localhost:8000
```

### Use Different Environment
```env
# Staging
VITE_API_BASE_URL=https://staging-api-id.execute-api.ap-south-1.amazonaws.com

# Production
VITE_API_BASE_URL=https://prod-api-id.execute-api.ap-south-1.amazonaws.com
```

After changing `.env`, restart your dev server:
```bash
npm run dev
```

---

## 🐛 Troubleshooting

### CORS Errors

If you see CORS errors in the console:

**Problem**: `Access-Control-Allow-Origin` header missing

**Solution**: The API Gateway is already configured with CORS. If you still see errors:
1. Check that requests include proper headers
2. Verify the API Gateway CORS configuration in AWS console
3. Ensure you're not sending custom headers that aren't allowed

### 401 Unauthorized

**Problem**: API returns 401 status

**Solution**: 
- The current API doesn't require authentication
- If you add authentication later, update the API service to include auth tokens

### Network Timeout

**Problem**: Requests timeout after 30 seconds

**Solution**: Increase timeout in `frontend/src/config/api.ts`:
```typescript
export const API_CONFIG = {
  timeout: 60000, // 60 seconds
  // ...
}
```

### Empty Responses

**Problem**: API returns empty arrays `[]`

**Solution**: This is expected! The database is empty. Seed test data:
```bash
cd backend
python seed_data.py
```

---

## 📊 API Response Examples

### Market Prices Response
```json
{
  "item": "tomatoes",
  "prices": [
    {
      "item_name": "tomatoes",
      "mandi_name": "Azadpur",
      "price_per_kg": 30.0,
      "distance_km": 5.2,
      "timestamp": "2026-03-03T10:00:00Z"
    }
  ],
  "count": 1
}
```

### Transaction Response
```json
{
  "transaction_id": "txn-123",
  "vendor_id": "vendor-123",
  "item_name": "tomatoes",
  "quantity": 2.0,
  "unit": "kg",
  "price_per_unit": 25.0,
  "total_amount": 50.0,
  "timestamp": 1709460000,
  "recorded_via": "voice"
}
```

### Trust Score Response
```json
{
  "vendor_id": "vendor-123",
  "trust_score": 150,
  "tier": "Silver",
  "breakdown": {
    "transactions": 100,
    "marketplace_sales": 40,
    "consistency": 10
  }
}
```

---

## 🚀 Next Steps

### 1. Update Your Components

Replace any mock data or local API calls with the real API service:

```typescript
// Before (mock data)
const [prices, setPrices] = useState(mockPrices)

// After (real API)
const [prices, setPrices] = useState([])
useEffect(() => {
  apiService.get('/prices/tomatoes').then(setPrices)
}, [])
```

### 2. Add Error Handling

```typescript
try {
  const data = await apiService.get('/prices/tomatoes')
  setPrices(data.prices)
} catch (error) {
  console.error('API Error:', error)
  // Show error message to user
  setError('Failed to load prices. Please try again.')
}
```

### 3. Add Loading States

```typescript
const [loading, setLoading] = useState(true)

useEffect(() => {
  setLoading(true)
  apiService.get('/prices/tomatoes')
    .then(data => setPrices(data.prices))
    .catch(error => setError(error.message))
    .finally(() => setLoading(false))
}, [])
```

### 4. Implement Caching

```typescript
// Cache API responses to reduce calls
const cache = new Map()

async function getCachedPrices(item: string) {
  if (cache.has(item)) {
    return cache.get(item)
  }
  
  const data = await apiService.get(`/prices/${item}`)
  cache.set(item, data)
  return data
}
```

---

## 📝 Configuration Files Updated

✅ `frontend/.env` - Updated with production API URL  
✅ `frontend/.env.example` - Updated with production API URL  
✅ `frontend/src/config/api.ts` - Already configured to use env vars  
✅ `frontend/src/services/api.ts` - Already set up with axios client  

---

## 🎉 You're All Set!

Your frontend is now connected to the AWS backend. All API calls will go through the API Gateway to your Lambda functions.

**API Base URL**: `https://ji5ymmu4g7.execute-api.ap-south-1.amazonaws.com`

Start your frontend and test the integration:

```bash
cd frontend
npm run dev
```

Happy coding! 🚀

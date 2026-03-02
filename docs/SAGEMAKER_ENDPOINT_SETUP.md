# SageMaker Endpoint Setup for Produce Freshness Classification

## Overview

This document describes the SageMaker endpoint setup for produce freshness classification in the Smart Vendors application. The endpoint classifies produce images into three categories: Fresh, B-Grade, and Waste.

## Architecture

```
┌─────────────────┐
│  Lambda Function│
│  (classify_     │
│   freshness)    │
└────────┬────────┘
         │
         │ 1. Upload image to S3
         ▼
┌─────────────────┐
│   S3 Bucket     │
│  (images)       │
└────────┬────────┘
         │
         │ 2. Invoke endpoint with S3 URI
         ▼
┌─────────────────┐
│  SageMaker      │
│  Endpoint       │
│  (produce-      │
│   freshness-    │
│   classifier)   │
└────────┬────────┘
         │
         │ 3. Return classification
         ▼
┌─────────────────┐
│  Response       │
│  - category     │
│  - confidence   │
│  - shelf_life   │
│  - suggestions  │
└─────────────────┘
```

## Classification Logic

The endpoint implements confidence threshold mapping as per requirements:

| Confidence Score | Category | Shelf Life | Description |
|-----------------|----------|------------|-------------|
| > 0.7           | Fresh    | 48 hours   | Premium quality, sell at full price |
| 0.4 - 0.7       | B-Grade  | 12 hours   | Reduced quality, list on marketplace |
| < 0.4           | Waste    | 0 hours    | Not suitable for sale, compost |

## Demo Mode

For hackathon demonstration purposes, the system includes a **demo mode** that uses mock classification when:
- `DEMO_MODE=true` environment variable is set
- SageMaker endpoint is unavailable
- Endpoint invocation fails

Demo mode features:
- **Deterministic**: Same image always returns same classification
- **Realistic distribution**: 50% Fresh, 30% B-Grade, 20% Waste
- **Proper thresholds**: Respects confidence threshold logic
- **Flagged results**: Includes `"mock": true` in response

## Deployment Options

### Option 1: Use Pre-trained Model (Recommended for Hackathon)

For rapid deployment, use a pre-trained image classification model:

1. **Use AWS Marketplace Model**:
   ```bash
   # Subscribe to a pre-trained image classification model
   # Example: ResNet-50 or MobileNet from AWS Marketplace
   ```

2. **Deploy to SageMaker Endpoint**:
   ```python
   import boto3
   
   sagemaker = boto3.client('sagemaker')
   
   # Create endpoint configuration
   sagemaker.create_endpoint_config(
       EndpointConfigName='produce-freshness-config',
       ProductionVariants=[{
           'VariantName': 'AllTraffic',
           'ModelName': 'produce-freshness-model',
           'InitialInstanceCount': 1,
           'InstanceType': 'ml.t2.medium'
       }]
   )
   
   # Create endpoint
   sagemaker.create_endpoint(
       EndpointName='produce-freshness-classifier',
       EndpointConfigName='produce-freshness-config'
   )
   ```

3. **Set Environment Variable**:
   ```bash
   export SAGEMAKER_ENDPOINT_NAME=produce-freshness-classifier
   ```

### Option 2: Train Custom Model

For production deployment, train a custom model:

1. **Prepare Training Data**:
   - Collect produce images labeled as Fresh, B-Grade, Waste
   - Upload to S3 bucket
   - Create manifest file

2. **Train Model**:
   ```python
   import sagemaker
   from sagemaker.image_uris import retrieve
   
   # Use built-in image classification algorithm
   training_image = retrieve('image-classification', region='ap-south-1')
   
   estimator = sagemaker.estimator.Estimator(
       training_image,
       role='SageMakerExecutionRole',
       instance_count=1,
       instance_type='ml.p3.2xlarge',
       output_path='s3://smart-vendors-ml-models/output'
   )
   
   estimator.fit({
       'train': 's3://smart-vendors-ml-models/training-data',
       'validation': 's3://smart-vendors-ml-models/validation-data'
   })
   ```

3. **Deploy Model**:
   ```python
   predictor = estimator.deploy(
       initial_instance_count=1,
       instance_type='ml.t2.medium',
       endpoint_name='produce-freshness-classifier'
   )
   ```

### Option 3: Use Demo Mode (Fastest for Hackathon)

For immediate demonstration without SageMaker setup:

1. **Enable Demo Mode**:
   ```bash
   export DEMO_MODE=true
   ```

2. **Deploy Lambda Functions**:
   - Lambda will automatically use mock classification
   - No SageMaker endpoint required
   - Results are deterministic and realistic

## Input/Output Format

### Input Payload

```json
{
  "image_uri": "s3://smart-vendors-images/vendor-123/image-456.jpg"
}
```

### Output Format

```json
{
  "category": "Fresh",
  "confidence": 0.85,
  "shelf_life_hours": 48,
  "suggestions": [
    "Sell at premium price",
    "Display prominently",
    "Store in cool place"
  ]
}
```

## Error Handling

The SageMaker client implements robust error handling:

1. **Endpoint Not Found**: Falls back to mock classification
2. **Connection Timeout**: Falls back to mock classification
3. **Invalid Response**: Logs warning, uses default confidence (0.5)
4. **Client Initialization Failure**: Automatically enables demo mode

All errors are logged for debugging while maintaining service availability.

## Testing

The implementation includes comprehensive property-based tests:

```bash
# Run all freshness classification tests
pytest tests/test_freshness_classification_property.py -v

# Run with coverage
pytest tests/test_freshness_classification_property.py --cov=shared.aws.sagemaker_client
```

### Test Coverage

- ✅ Valid category classification (Fresh/B-Grade/Waste)
- ✅ Confidence threshold mapping (>0.7, 0.4-0.7, <0.4)
- ✅ Mock classification consistency
- ✅ Fallback on error
- ✅ End-to-end service integration
- ✅ Suggestions for each category
- ✅ Demo mode functionality

## Cost Optimization

For hackathon/demo purposes:

1. **Use smallest instance**: `ml.t2.medium` ($0.065/hour)
2. **Enable auto-scaling**: Scale to zero when not in use
3. **Use demo mode**: No SageMaker costs
4. **Delete endpoint after demo**: Avoid ongoing charges

```bash
# Delete endpoint after hackathon
aws sagemaker delete-endpoint --endpoint-name produce-freshness-classifier
aws sagemaker delete-endpoint-config --endpoint-config-name produce-freshness-config
```

## Environment Variables

Required environment variables:

```bash
# AWS Configuration
AWS_REGION=ap-south-1

# SageMaker Configuration
SAGEMAKER_ENDPOINT_NAME=produce-freshness-classifier

# Demo Mode (optional)
DEMO_MODE=false

# S3 Buckets
S3_IMAGES_BUCKET=smart-vendors-images-dev
```

## Monitoring

Monitor endpoint performance:

```bash
# Check endpoint status
aws sagemaker describe-endpoint --endpoint-name produce-freshness-classifier

# View CloudWatch metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/SageMaker \
  --metric-name ModelLatency \
  --dimensions Name=EndpointName,Value=produce-freshness-classifier \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Average
```

## Troubleshooting

### Issue: Endpoint returns 404

**Solution**: Verify endpoint exists and name matches environment variable
```bash
aws sagemaker list-endpoints
```

### Issue: High latency

**Solution**: 
- Use larger instance type
- Enable endpoint auto-scaling
- Implement caching for repeated images

### Issue: Classification accuracy low

**Solution**:
- Retrain model with more diverse data
- Adjust confidence thresholds
- Use ensemble of multiple models

## Next Steps

1. **For Hackathon Demo**: Use demo mode (fastest)
2. **For MVP**: Deploy pre-trained model from AWS Marketplace
3. **For Production**: Train custom model with real vendor data

## References

- [AWS SageMaker Documentation](https://docs.aws.amazon.com/sagemaker/)
- [SageMaker Python SDK](https://sagemaker.readthedocs.io/)
- [Built-in Image Classification Algorithm](https://docs.aws.amazon.com/sagemaker/latest/dg/image-classification.html)

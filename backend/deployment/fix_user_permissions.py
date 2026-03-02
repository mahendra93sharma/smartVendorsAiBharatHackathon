"""
Add AWS service permissions to the current IAM user.

This fixes permissions for the user running deployment scripts.
"""

import sys
import json
import boto3
from botocore.exceptions import ClientError


def get_current_user():
    """Get current IAM user information."""
    sts = boto3.client('sts')
    identity = sts.get_caller_identity()
    
    # Extract user name from ARN
    arn = identity['Arn']
    if ':user/' in arn:
        user_name = arn.split(':user/')[-1]
        return user_name, identity['Account']
    else:
        return None, identity['Account']


def create_policy_document():
    """Create policy document with all required permissions."""
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "BedrockAccess",
                "Effect": "Allow",
                "Action": [
                    "bedrock:*"
                ],
                "Resource": "*"
            },
            {
                "Sid": "TranscribeAccess",
                "Effect": "Allow",
                "Action": [
                    "transcribe:*"
                ],
                "Resource": "*"
            },
            {
                "Sid": "SageMakerAccess",
                "Effect": "Allow",
                "Action": [
                    "sagemaker:InvokeEndpoint",
                    "sagemaker:DescribeEndpoint",
                    "sagemaker:ListEndpoints"
                ],
                "Resource": "*"
            }
        ]
    }


def attach_managed_policy(iam_client, user_name, policy_arn):
    """Attach a managed policy to user."""
    try:
        iam_client.attach_user_policy(
            UserName=user_name,
            PolicyArn=policy_arn
        )
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            return True  # Already attached
        print(f"  ✗ Failed to attach policy: {e}")
        return False


def create_and_attach_inline_policy(iam_client, user_name):
    """Create and attach inline policy to user."""
    policy_name = "SmartVendorsAIServicesAccess"
    policy_document = create_policy_document()
    
    try:
        iam_client.put_user_policy(
            UserName=user_name,
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_document)
        )
        print(f"  ✓ Created inline policy: {policy_name}")
        return True
    except ClientError as e:
        print(f"  ✗ Failed to create inline policy: {e}")
        return False


def main():
    """Main function."""
    print("🔧 IAM User Permissions Fixer")
    print("="*70 + "\n")
    
    # Get current user
    user_name, account_id = get_current_user()
    
    if not user_name:
        print("✗ Could not determine IAM user name")
        print("  You might be using an IAM role instead of a user")
        print("  This script is for IAM users only")
        return 1
    
    print(f"Current IAM User: {user_name}")
    print(f"AWS Account: {account_id}\n")
    
    iam_client = boto3.client('iam')
    
    # Add permissions
    print("🔧 Adding AI service permissions to user...")
    
    success = create_and_attach_inline_policy(iam_client, user_name)
    
    if success:
        print("\n✓ Permissions added successfully!")
        print("\n⏳ Waiting 5 seconds for permissions to propagate...")
        import time
        time.sleep(5)
        
        # Verify
        print("\n🔍 Verifying access...")
        
        # Test Transcribe
        try:
            transcribe = boto3.client('transcribe', region_name='ap-south-1')
            transcribe.list_transcription_jobs(MaxResults=1)
            print("  ✓ Transcribe access: Working")
        except ClientError as e:
            print(f"  ⚠️  Transcribe access: Still denied")
            print(f"     Error: {e.response['Error']['Code']}")
        
        # Test Bedrock
        try:
            bedrock = boto3.client('bedrock', region_name='ap-south-1')
            response = bedrock.list_foundation_models()
            print("  ✓ Bedrock access: Working")
            
            claude_models = [
                m for m in response.get('modelSummaries', [])
                if 'claude' in m.get('modelId', '').lower()
            ]
            if claude_models:
                print(f"    Found {len(claude_models)} Claude models")
            else:
                print("    ⚠️  No Claude models - need to request model access")
        except ClientError as e:
            print(f"  ⚠️  Bedrock access: {e.response['Error']['Code']}")
        
        print("\n" + "="*70)
        print("✓ User permissions updated!")
        print("="*70)
        print("""
Next steps:

1. For Bedrock: Request model access in AWS Console
   → https://console.aws.amazon.com/bedrock/
   → Click "Model access" → Enable Claude models

2. For Transcribe: Should work now (permissions added)

3. For SageMaker: Using demo mode (no action needed)

Run the prerequisite validator to verify:
  python deployment/validate_prerequisites.py
""")
        return 0
    else:
        print("\n✗ Failed to add permissions")
        return 1


if __name__ == "__main__":
    sys.exit(main())

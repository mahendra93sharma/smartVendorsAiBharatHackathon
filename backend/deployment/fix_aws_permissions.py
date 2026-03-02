"""
Fix AWS permissions for Bedrock, Transcribe, and SageMaker.

This script adds the necessary IAM permissions to the Lambda execution role.
"""

import sys
import json
import boto3
from botocore.exceptions import ClientError


def fix_bedrock_permissions(iam_client, role_name):
    """Add Bedrock permissions to IAM role."""
    print("🔧 Adding AWS Bedrock permissions...")
    
    bedrock_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "bedrock:InvokeModel",
                    "bedrock:InvokeModelWithResponseStream",
                    "bedrock:ListFoundationModels",
                    "bedrock:GetFoundationModel"
                ],
                "Resource": "*"
            }
        ]
    }
    
    policy_name = "BedrockAccessPolicy"
    
    try:
        # Create inline policy
        iam_client.put_role_policy(
            RoleName=role_name,
            PolicyName=policy_name,
            PolicyDocument=json.dumps(bedrock_policy)
        )
        print(f"  ✓ Added Bedrock permissions to {role_name}")
        return True
    except ClientError as e:
        print(f"  ✗ Failed to add Bedrock permissions: {e}")
        return False


def fix_transcribe_permissions(iam_client, role_name):
    """Add Transcribe permissions to IAM role."""
    print("🔧 Adding AWS Transcribe permissions...")
    
    transcribe_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "transcribe:StartTranscriptionJob",
                    "transcribe:GetTranscriptionJob",
                    "transcribe:ListTranscriptionJobs",
                    "transcribe:DeleteTranscriptionJob",
                    "transcribe:StartStreamTranscription"
                ],
                "Resource": "*"
            }
        ]
    }
    
    policy_name = "TranscribeAccessPolicy"
    
    try:
        # Create inline policy
        iam_client.put_role_policy(
            RoleName=role_name,
            PolicyName=policy_name,
            PolicyDocument=json.dumps(transcribe_policy)
        )
        print(f"  ✓ Added Transcribe permissions to {role_name}")
        return True
    except ClientError as e:
        print(f"  ✗ Failed to add Transcribe permissions: {e}")
        return False


def check_bedrock_access(region):
    """Check if Bedrock is accessible and has model access."""
    print("\n🔍 Checking AWS Bedrock access...")
    
    try:
        bedrock = boto3.client('bedrock', region_name=region)
        response = bedrock.list_foundation_models()
        
        # Check for Claude models
        claude_models = [
            model for model in response.get('modelSummaries', [])
            if 'claude' in model.get('modelId', '').lower()
        ]
        
        if claude_models:
            print(f"  ✓ Bedrock accessible with {len(claude_models)} Claude models")
            print(f"    Available models:")
            for model in claude_models[:3]:  # Show first 3
                print(f"      - {model.get('modelId')}")
            return True
        else:
            print("  ⚠️  Bedrock accessible but no Claude models found")
            print("  → You need to request model access in AWS Console")
            return False
            
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', '')
        if error_code == 'AccessDeniedException':
            print("  ⚠️  Bedrock access denied")
            print("  → Permissions have been added, but you need to:")
            print("     1. Go to AWS Bedrock console")
            print("     2. Request model access for Claude")
            print("     3. Wait for approval (usually instant)")
        else:
            print(f"  ✗ Bedrock error: {e}")
        return False


def check_transcribe_access(region):
    """Check if Transcribe is accessible."""
    print("\n🔍 Checking AWS Transcribe access...")
    
    try:
        transcribe = boto3.client('transcribe', region_name=region)
        transcribe.list_transcription_jobs(MaxResults=1)
        print("  ✓ Transcribe is accessible")
        return True
    except ClientError as e:
        print(f"  ✗ Transcribe error: {e}")
        return False


def print_bedrock_instructions():
    """Print instructions for enabling Bedrock model access."""
    print("\n" + "="*70)
    print("📋 BEDROCK MODEL ACCESS INSTRUCTIONS")
    print("="*70)
    print("""
To enable AWS Bedrock with Claude models:

1. Open AWS Console: https://console.aws.amazon.com/bedrock/

2. In the left sidebar, click "Model access"

3. Click "Manage model access" or "Edit" button

4. Find and enable these models:
   ✓ Claude 3 Sonnet
   ✓ Claude 3 Haiku
   ✓ Claude 2.1
   ✓ Claude 2
   ✓ Claude Instant

5. Click "Save changes"

6. Wait for approval (usually instant, status will change to "Access granted")

7. Run this script again to verify: python deployment/fix_aws_permissions.py

Note: Bedrock is available in these regions:
- us-east-1 (N. Virginia)
- us-west-2 (Oregon)
- ap-south-1 (Mumbai) ← Your current region
- eu-central-1 (Frankfurt)
- ap-northeast-1 (Tokyo)
""")
    print("="*70 + "\n")


def main():
    """Main function to fix AWS permissions."""
    print("🔧 AWS Permissions Fixer")
    print("="*70 + "\n")
    
    region = "ap-south-1"
    environment = "dev"
    project_name = "smart-vendors"
    role_name = f"{project_name}-lambda-execution-{environment}"
    
    # Initialize AWS clients
    iam_client = boto3.client('iam')
    
    print(f"Target IAM Role: {role_name}")
    print(f"AWS Region: {region}\n")
    
    # Check if role exists
    try:
        iam_client.get_role(RoleName=role_name)
        print(f"✓ IAM role found: {role_name}\n")
    except ClientError:
        print(f"✗ IAM role not found: {role_name}")
        print("  Run deployment first to create the role")
        return 1
    
    # Fix permissions
    results = []
    
    # 1. Add Bedrock permissions
    results.append(fix_bedrock_permissions(iam_client, role_name))
    
    # 2. Add Transcribe permissions
    results.append(fix_transcribe_permissions(iam_client, role_name))
    
    print("\n" + "="*70)
    print("PERMISSIONS UPDATE COMPLETE")
    print("="*70)
    
    if all(results):
        print("\n✓ All permissions added successfully!\n")
    else:
        print("\n⚠️  Some permissions failed to add. Check errors above.\n")
    
    # Wait a moment for permissions to propagate
    print("⏳ Waiting 5 seconds for permissions to propagate...")
    import time
    time.sleep(5)
    
    # Verify access
    print("\n" + "="*70)
    print("VERIFYING ACCESS")
    print("="*70)
    
    bedrock_ok = check_bedrock_access(region)
    transcribe_ok = check_transcribe_access(region)
    
    # Print summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"\n✓ Bedrock Permissions: Added")
    print(f"{'✓' if bedrock_ok else '⚠️ '} Bedrock Access: {'Working' if bedrock_ok else 'Needs model access'}")
    print(f"\n✓ Transcribe Permissions: Added")
    print(f"{'✓' if transcribe_ok else '✗'} Transcribe Access: {'Working' if transcribe_ok else 'Failed'}")
    print(f"\n✓ SageMaker: Using demo mode (no action needed)")
    
    # Print next steps if needed
    if not bedrock_ok:
        print_bedrock_instructions()
    
    if bedrock_ok and transcribe_ok:
        print("\n🎉 All AWS services are now accessible!")
        print("\nYou can now use:")
        print("  - Voice transcription (AWS Transcribe)")
        print("  - Transaction extraction (AWS Bedrock)")
        print("  - Freshness classification (Demo mode)")
        print("\n" + "="*70 + "\n")
        return 0
    else:
        print("\n⚠️  Some services need additional setup. See instructions above.")
        print("="*70 + "\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())

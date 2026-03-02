"""
Prerequisite validation for AWS deployment.

Validates that all required tools, credentials, and services are available
before attempting deployment.
"""

import subprocess
import sys
import os
from typing import List, Tuple, Optional
from dataclasses import dataclass
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


@dataclass
class ValidationResult:
    """Result of a validation check."""
    check_name: str
    passed: bool
    message: str
    remediation: Optional[str] = None


class PrerequisiteValidator:
    """Validates deployment prerequisites."""
    
    def __init__(self, aws_region: str = "ap-south-1"):
        """
        Initialize validator.
        
        Args:
            aws_region: AWS region for deployment
        """
        self.aws_region = aws_region
        self.results: List[ValidationResult] = []
    
    def validate_all(self) -> bool:
        """
        Run all validation checks.
        
        Returns:
            True if all checks pass, False otherwise
        """
        print("🔍 Validating deployment prerequisites...\n")
        
        # Check Python version
        self._check_python_version()
        
        # Check AWS CLI
        self._check_aws_cli()
        
        # Check AWS credentials
        self._check_aws_credentials()
        
        # Check Terraform
        self._check_terraform()
        
        # Check required Python packages
        self._check_python_packages()
        
        # Check AWS services availability
        self._check_aws_services()
        
        # Print results
        self._print_results()
        
        # Return overall status
        return all(r.passed for r in self.results)
    
    def _check_python_version(self):
        """Check Python version is 3.11 or higher."""
        version = sys.version_info
        if version.major == 3 and version.minor >= 11:
            self.results.append(ValidationResult(
                check_name="Python Version",
                passed=True,
                message=f"Python {version.major}.{version.minor}.{version.micro} ✓"
            ))
        else:
            self.results.append(ValidationResult(
                check_name="Python Version",
                passed=False,
                message=f"Python {version.major}.{version.minor}.{version.micro} (requires 3.11+)",
                remediation="Install Python 3.11 or higher: https://www.python.org/downloads/"
            ))
    
    def _check_aws_cli(self):
        """Check AWS CLI is installed."""
        try:
            result = subprocess.run(
                ["aws", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                self.results.append(ValidationResult(
                    check_name="AWS CLI",
                    passed=True,
                    message=f"{version} ✓"
                ))
            else:
                self._add_aws_cli_failure()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self._add_aws_cli_failure()
    
    def _add_aws_cli_failure(self):
        """Add AWS CLI failure result."""
        self.results.append(ValidationResult(
            check_name="AWS CLI",
            passed=False,
            message="AWS CLI not found",
            remediation="Install AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
        ))
    
    def _check_aws_credentials(self):
        """Check AWS credentials are configured."""
        try:
            # Try to get caller identity
            sts = boto3.client('sts', region_name=self.aws_region)
            identity = sts.get_caller_identity()
            account_id = identity['Account']
            user_arn = identity['Arn']
            
            self.results.append(ValidationResult(
                check_name="AWS Credentials",
                passed=True,
                message=f"Authenticated as {user_arn} (Account: {account_id}) ✓"
            ))
        except NoCredentialsError:
            self.results.append(ValidationResult(
                check_name="AWS Credentials",
                passed=False,
                message="No AWS credentials found",
                remediation="Configure AWS credentials:\n"
                           "  1. Run: aws configure\n"
                           "  2. Or set environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY\n"
                           "  3. Or use IAM role (if running on EC2/ECS)"
            ))
        except ClientError as e:
            self.results.append(ValidationResult(
                check_name="AWS Credentials",
                passed=False,
                message=f"AWS credentials error: {e}",
                remediation="Check your AWS credentials and permissions"
            ))
    
    def _check_terraform(self):
        """Check Terraform is installed."""
        try:
            result = subprocess.run(
                ["terraform", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                self.results.append(ValidationResult(
                    check_name="Terraform",
                    passed=True,
                    message=f"{version} ✓"
                ))
            else:
                self._add_terraform_failure()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self._add_terraform_failure()
    
    def _add_terraform_failure(self):
        """Add Terraform failure result."""
        self.results.append(ValidationResult(
            check_name="Terraform",
            passed=False,
            message="Terraform not found",
            remediation="Install Terraform: https://developer.hashicorp.com/terraform/downloads"
        ))
    
    def _check_python_packages(self):
        """Check required Python packages are installed."""
        required_packages = [
            "boto3",
            "botocore",
            "python-dotenv",
            "pydantic",
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
            except ImportError:
                missing_packages.append(package)
        
        if not missing_packages:
            self.results.append(ValidationResult(
                check_name="Python Packages",
                passed=True,
                message=f"All required packages installed ✓"
            ))
        else:
            self.results.append(ValidationResult(
                check_name="Python Packages",
                passed=False,
                message=f"Missing packages: {', '.join(missing_packages)}",
                remediation=f"Install missing packages:\n"
                           f"  pip install {' '.join(missing_packages)}\n"
                           f"  Or: pip install -r backend/requirements.txt"
            ))
    
    def _check_aws_services(self):
        """Check AWS services are available in the region."""
        # Check Bedrock
        self._check_bedrock()
        
        # Check Transcribe
        self._check_transcribe()
        
        # Check SageMaker (optional - can use demo mode)
        self._check_sagemaker()
    
    def _check_bedrock(self):
        """Check AWS Bedrock service availability."""
        try:
            bedrock = boto3.client('bedrock', region_name=self.aws_region)
            # Try to list foundation models
            response = bedrock.list_foundation_models()
            
            # Check if Claude model is available
            claude_available = any(
                'claude' in model.get('modelId', '').lower()
                for model in response.get('modelSummaries', [])
            )
            
            if claude_available:
                self.results.append(ValidationResult(
                    check_name="AWS Bedrock",
                    passed=True,
                    message=f"Bedrock available in {self.aws_region} with Claude models ✓"
                ))
            else:
                self.results.append(ValidationResult(
                    check_name="AWS Bedrock",
                    passed=False,
                    message=f"Bedrock available but Claude models not found in {self.aws_region}",
                    remediation="Request access to Claude models in AWS Bedrock console:\n"
                               "  https://console.aws.amazon.com/bedrock/home#/modelaccess"
                ))
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code == 'AccessDeniedException':
                self.results.append(ValidationResult(
                    check_name="AWS Bedrock",
                    passed=False,
                    message=f"Bedrock access denied in {self.aws_region}",
                    remediation="Enable Bedrock in your AWS account:\n"
                               "  1. Go to AWS Bedrock console\n"
                               "  2. Request model access\n"
                               "  3. Wait for approval (usually instant for Claude)"
                ))
            else:
                self.results.append(ValidationResult(
                    check_name="AWS Bedrock",
                    passed=False,
                    message=f"Bedrock error: {e}",
                    remediation=f"Check if Bedrock is available in {self.aws_region}"
                ))
        except Exception as e:
            self.results.append(ValidationResult(
                check_name="AWS Bedrock",
                passed=False,
                message=f"Bedrock check failed: {e}",
                remediation="Verify AWS credentials and region configuration"
            ))
    
    def _check_transcribe(self):
        """Check AWS Transcribe service availability."""
        try:
            transcribe = boto3.client('transcribe', region_name=self.aws_region)
            # Try to list transcription jobs (should work even if empty)
            transcribe.list_transcription_jobs(MaxResults=1)
            
            self.results.append(ValidationResult(
                check_name="AWS Transcribe",
                passed=True,
                message=f"Transcribe available in {self.aws_region} ✓"
            ))
        except ClientError as e:
            self.results.append(ValidationResult(
                check_name="AWS Transcribe",
                passed=False,
                message=f"Transcribe error: {e}",
                remediation=f"Check if Transcribe is available in {self.aws_region}"
            ))
        except Exception as e:
            self.results.append(ValidationResult(
                check_name="AWS Transcribe",
                passed=False,
                message=f"Transcribe check failed: {e}",
                remediation="Verify AWS credentials and region configuration"
            ))
    
    def _check_sagemaker(self):
        """Check AWS SageMaker service availability (optional)."""
        try:
            sagemaker = boto3.client('sagemaker', region_name=self.aws_region)
            # Try to list endpoints
            sagemaker.list_endpoints(MaxResults=1)
            
            # Check if specific endpoint exists
            endpoint_name = os.getenv('SAGEMAKER_ENDPOINT_NAME', 'produce-freshness-classifier')
            try:
                sagemaker.describe_endpoint(EndpointName=endpoint_name)
                self.results.append(ValidationResult(
                    check_name="AWS SageMaker",
                    passed=True,
                    message=f"SageMaker endpoint '{endpoint_name}' found ✓"
                ))
            except ClientError:
                # Endpoint doesn't exist, but that's okay - we can use demo mode
                self.results.append(ValidationResult(
                    check_name="AWS SageMaker",
                    passed=True,
                    message=f"SageMaker available (endpoint not found, will use demo mode) ⚠️"
                ))
        except ClientError as e:
            self.results.append(ValidationResult(
                check_name="AWS SageMaker",
                passed=True,  # Not critical - can use demo mode
                message=f"SageMaker not available (will use demo mode) ⚠️"
            ))
        except Exception as e:
            self.results.append(ValidationResult(
                check_name="AWS SageMaker",
                passed=True,  # Not critical - can use demo mode
                message=f"SageMaker check skipped (will use demo mode) ⚠️"
            ))
    
    def _print_results(self):
        """Print validation results."""
        print("\n" + "="*70)
        print("VALIDATION RESULTS")
        print("="*70 + "\n")
        
        for result in self.results:
            status = "✓ PASS" if result.passed else "✗ FAIL"
            print(f"{status:8} | {result.check_name:20} | {result.message}")
            if result.remediation and not result.passed:
                print(f"         | {'':20} | Remediation:")
                for line in result.remediation.split('\n'):
                    print(f"         | {'':20} |   {line}")
                print()
        
        print("="*70)
        
        passed_count = sum(1 for r in self.results if r.passed)
        total_count = len(self.results)
        
        if passed_count == total_count:
            print(f"✓ All {total_count} checks passed! Ready to deploy.")
        else:
            failed_count = total_count - passed_count
            print(f"✗ {failed_count} of {total_count} checks failed. Fix issues before deploying.")
        
        print("="*70 + "\n")


def main():
    """Main entry point for prerequisite validation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate AWS deployment prerequisites")
    parser.add_argument(
        "--region",
        default="ap-south-1",
        help="AWS region for deployment (default: ap-south-1)"
    )
    
    args = parser.parse_args()
    
    validator = PrerequisiteValidator(aws_region=args.region)
    success = validator.validate_all()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

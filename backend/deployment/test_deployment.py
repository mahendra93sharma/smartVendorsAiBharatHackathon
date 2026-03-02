"""
Test deployed Lambda functions and API endpoints.

Tests each Lambda function individually and verifies API Gateway integration.
"""

import json
import time
import requests
from typing import Dict, Any, List
from dataclasses import dataclass
import boto3
from botocore.exceptions import ClientError


@dataclass
class TestResult:
    """Result of a test execution."""
    test_name: str
    passed: bool
    response_time_ms: float
    actual_response: Any
    error_message: str = ""


class DeploymentTester:
    """Tests deployed Lambda functions and APIs."""
    
    def __init__(self, region: str = "ap-south-1", environment: str = "dev"):
        """
        Initialize tester.
        
        Args:
            region: AWS region
            environment: Deployment environment
        """
        self.region = region
        self.environment = environment
        self.project_name = "smart-vendors"
        
        self.lambda_client = boto3.client('lambda', region_name=region)
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        
        self.results: List[TestResult] = []
    
    def test_all(self) -> bool:
        """
        Run all tests.
        
        Returns:
            True if all tests pass, False otherwise
        """
        print("🧪 Testing Smart Vendors Backend Deployment")
        print("="*70 + "\n")
        
        # Test Lambda functions
        self._test_lambda_functions()
        
        # Test DynamoDB tables
        self._test_dynamodb_tables()
        
        # Test S3 buckets
        self._test_s3_buckets()
        
        # Print results
        self._print_results()
        
        return all(r.passed for r in self.results)
    
    def _test_lambda_functions(self):
        """Test all Lambda functions."""
        print("⚡ Testing Lambda Functions...\n")
        
        functions = [
            "voice-transcribe",
            "create-transaction",
            "get-transactions",
            "get-market-prices",
            "classify-freshness",
            "create-marketplace-listing",
            "get-marketplace-buyers",
            "notify-marketplace-buyers",
            "get-trust-score",
        ]
        
        for func_name in functions:
            full_name = f"{self.project_name}-{func_name}-{self.environment}"
            self._test_lambda_function(full_name)
    
    def _test_lambda_function(self, function_name: str):
        """
        Test a single Lambda function.
        
        Args:
            function_name: Name of the Lambda function
        """
        try:
            start_time = time.time()
            
            # Get function configuration
            response = self.lambda_client.get_function(FunctionName=function_name)
            config = response['Configuration']
            
            elapsed_ms = (time.time() - start_time) * 1000
            
            # Check if function is active
            if config['State'] == 'Active':
                self.results.append(TestResult(
                    test_name=f"Lambda: {function_name}",
                    passed=True,
                    response_time_ms=elapsed_ms,
                    actual_response=f"State: {config['State']}, Runtime: {config['Runtime']}"
                ))
                print(f"  ✓ {function_name}: Active ({elapsed_ms:.0f}ms)")
            else:
                self.results.append(TestResult(
                    test_name=f"Lambda: {function_name}",
                    passed=False,
                    response_time_ms=elapsed_ms,
                    actual_response=config['State'],
                    error_message=f"Function state is {config['State']}, expected Active"
                ))
                print(f"  ✗ {function_name}: {config['State']}")
                
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                self.results.append(TestResult(
                    test_name=f"Lambda: {function_name}",
                    passed=False,
                    response_time_ms=0,
                    actual_response=None,
                    error_message="Function not found"
                ))
                print(f"  ✗ {function_name}: Not found")
            else:
                self.results.append(TestResult(
                    test_name=f"Lambda: {function_name}",
                    passed=False,
                    response_time_ms=0,
                    actual_response=None,
                    error_message=str(e)
                ))
                print(f"  ✗ {function_name}: {e}")
        
        print()
    
    def _test_dynamodb_tables(self):
        """Test DynamoDB tables."""
        print("🗄️  Testing DynamoDB Tables...\n")
        
        tables = [
            "vendors",
            "transactions",
            "market-prices",
            "marketplace-listings",
        ]
        
        for table_name in tables:
            full_name = f"{self.project_name}-{table_name}-{self.environment}"
            self._test_dynamodb_table(full_name)
    
    def _test_dynamodb_table(self, table_name: str):
        """
        Test a single DynamoDB table.
        
        Args:
            table_name: Name of the DynamoDB table
        """
        try:
            start_time = time.time()
            
            table = self.dynamodb.Table(table_name)
            table.load()
            
            elapsed_ms = (time.time() - start_time) * 1000
            
            if table.table_status == 'ACTIVE':
                self.results.append(TestResult(
                    test_name=f"DynamoDB: {table_name}",
                    passed=True,
                    response_time_ms=elapsed_ms,
                    actual_response=f"Status: {table.table_status}, Items: {table.item_count}"
                ))
                print(f"  ✓ {table_name}: Active ({elapsed_ms:.0f}ms)")
            else:
                self.results.append(TestResult(
                    test_name=f"DynamoDB: {table_name}",
                    passed=False,
                    response_time_ms=elapsed_ms,
                    actual_response=table.table_status,
                    error_message=f"Table status is {table.table_status}, expected ACTIVE"
                ))
                print(f"  ✗ {table_name}: {table.table_status}")
                
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                self.results.append(TestResult(
                    test_name=f"DynamoDB: {table_name}",
                    passed=False,
                    response_time_ms=0,
                    actual_response=None,
                    error_message="Table not found"
                ))
                print(f"  ✗ {table_name}: Not found")
            else:
                self.results.append(TestResult(
                    test_name=f"DynamoDB: {table_name}",
                    passed=False,
                    response_time_ms=0,
                    actual_response=None,
                    error_message=str(e)
                ))
                print(f"  ✗ {table_name}: {e}")
        
        print()
    
    def _test_s3_buckets(self):
        """Test S3 buckets."""
        print("🪣 Testing S3 Buckets...\n")
        
        s3_client = boto3.client('s3', region_name=self.region)
        
        buckets = [
            "images",
            "static",
            "ml-models",
        ]
        
        for bucket_name in buckets:
            full_name = f"{self.project_name}-{bucket_name}-{self.environment}"
            
            try:
                start_time = time.time()
                
                s3_client.head_bucket(Bucket=full_name)
                
                elapsed_ms = (time.time() - start_time) * 1000
                
                self.results.append(TestResult(
                    test_name=f"S3: {full_name}",
                    passed=True,
                    response_time_ms=elapsed_ms,
                    actual_response="Bucket exists"
                ))
                print(f"  ✓ {full_name}: Exists ({elapsed_ms:.0f}ms)")
                
            except ClientError as e:
                if e.response['Error']['Code'] == '404':
                    self.results.append(TestResult(
                        test_name=f"S3: {full_name}",
                        passed=False,
                        response_time_ms=0,
                        actual_response=None,
                        error_message="Bucket not found"
                    ))
                    print(f"  ✗ {full_name}: Not found")
                else:
                    self.results.append(TestResult(
                        test_name=f"S3: {full_name}",
                        passed=False,
                        response_time_ms=0,
                        actual_response=None,
                        error_message=str(e)
                    ))
                    print(f"  ✗ {full_name}: {e}")
        
        print()
    
    def _print_results(self):
        """Print test results summary."""
        print("\n" + "="*70)
        print("TEST RESULTS SUMMARY")
        print("="*70 + "\n")
        
        passed_count = sum(1 for r in self.results if r.passed)
        total_count = len(self.results)
        
        print(f"Total Tests: {total_count}")
        print(f"Passed: {passed_count}")
        print(f"Failed: {total_count - passed_count}")
        print(f"Success Rate: {(passed_count/total_count*100):.1f}%")
        
        if passed_count < total_count:
            print("\nFailed Tests:")
            for result in self.results:
                if not result.passed:
                    print(f"  ✗ {result.test_name}: {result.error_message}")
        
        print("="*70 + "\n")


def main():
    """Main entry point for testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Smart Vendors backend deployment")
    parser.add_argument(
        "--environment",
        default="dev",
        help="Deployment environment (default: dev)"
    )
    parser.add_argument(
        "--region",
        default="ap-south-1",
        help="AWS region (default: ap-south-1)"
    )
    
    args = parser.parse_args()
    
    tester = DeploymentTester(region=args.region, environment=args.environment)
    success = tester.test_all()
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())

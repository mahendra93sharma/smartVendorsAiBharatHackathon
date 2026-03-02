#!/usr/bin/env node

/**
 * Test script to verify AWS API Gateway integration
 * 
 * Run: node test-api-integration.js
 */

const API_BASE_URL = 'https://ji5ymmu4g7.execute-api.ap-south-1.amazonaws.com';

const tests = [
  {
    name: 'Get Market Prices',
    method: 'GET',
    endpoint: '/prices/tomatoes',
    expectedStatus: 200,
  },
  {
    name: 'Get Vendor Transactions',
    method: 'GET',
    endpoint: '/transactions/vendor-123',
    expectedStatus: 200,
  },
  {
    name: 'Get Trust Score',
    method: 'GET',
    endpoint: '/trust-score/vendor-123',
    expectedStatus: 200,
  },
  {
    name: 'Get Marketplace Buyers',
    method: 'GET',
    endpoint: '/marketplace/buyers',
    expectedStatus: 200,
  },
];

async function testEndpoint(test) {
  const url = `${API_BASE_URL}${test.endpoint}`;
  
  try {
    const response = await fetch(url, {
      method: test.method,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();
    const passed = response.status === test.expectedStatus;

    return {
      ...test,
      passed,
      status: response.status,
      response: data,
    };
  } catch (error) {
    return {
      ...test,
      passed: false,
      error: error.message,
    };
  }
}

async function runTests() {
  console.log('🧪 Testing AWS API Gateway Integration\n');
  console.log(`API Base URL: ${API_BASE_URL}\n`);
  console.log('='  .repeat(70));

  const results = [];

  for (const test of tests) {
    process.stdout.write(`Testing: ${test.name}... `);
    const result = await testEndpoint(test);
    results.push(result);

    if (result.passed) {
      console.log('✅ PASS');
      console.log(`  Status: ${result.status}`);
      console.log(`  Response:`, JSON.stringify(result.response).substring(0, 100));
    } else {
      console.log('❌ FAIL');
      if (result.error) {
        console.log(`  Error: ${result.error}`);
      } else {
        console.log(`  Expected: ${test.expectedStatus}, Got: ${result.status}`);
      }
    }
    console.log();
  }

  console.log('='  .repeat(70));
  
  const passed = results.filter(r => r.passed).length;
  const total = results.length;
  const percentage = ((passed / total) * 100).toFixed(1);

  console.log(`\n📊 Results: ${passed}/${total} tests passed (${percentage}%)\n`);

  if (passed === total) {
    console.log('✅ All tests passed! API integration is working correctly.\n');
    process.exit(0);
  } else {
    console.log('⚠️  Some tests failed. Check the errors above.\n');
    process.exit(1);
  }
}

// Run tests
runTests().catch(error => {
  console.error('❌ Test runner failed:', error);
  process.exit(1);
});

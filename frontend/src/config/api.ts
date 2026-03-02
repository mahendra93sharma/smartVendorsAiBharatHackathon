export const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  gatewayURL: import.meta.env.VITE_API_GATEWAY_URL || 'http://localhost:8000',
  region: import.meta.env.VITE_AWS_REGION || 'ap-south-1',
  timeout: 30000,
}

export const FEATURE_FLAGS = {
  enableDemoMode: import.meta.env.VITE_ENABLE_DEMO_MODE === 'true',
  enableOfflineMode: import.meta.env.VITE_ENABLE_OFFLINE_MODE === 'true',
}

export const DEMO_CREDENTIALS = {
  username: 'demo_vendor',
  password: 'hackathon2024',
  vendorId: 'demo-vendor-001',
}

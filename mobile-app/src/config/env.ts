/**
 * Environment configuration
 * Uses react-native-config to load environment variables
 */

import Config from 'react-native-config';
import { EnvConfig } from '@types/index';

export const env: EnvConfig = {
  API_BASE_URL: Config.API_BASE_URL || 'https://api.example.com',
  AWS_REGION: Config.AWS_REGION || 'ap-south-1',
  S3_BUCKET_NAME: Config.S3_BUCKET_NAME || 'vendor-app-uploads',
  FIREBASE_PROJECT_ID: Config.FIREBASE_PROJECT_ID || 'vendor-app',
  APP_ENV: (Config.APP_ENV as 'development' | 'staging' | 'production') || 'development',
  DEMO_MODE: Config.DEMO_MODE === 'true',
};

export const isDevelopment = env.APP_ENV === 'development';
export const isProduction = env.APP_ENV === 'production';
export const isDemoMode = env.DEMO_MODE;

// API Configuration
export const API_CONFIG = {
  baseURL: env.API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
};

// Cache Configuration
export const CACHE_CONFIG = {
  TRANSACTIONS_TTL: 24 * 60 * 60 * 1000, // 24 hours
  PRICES_TTL: 60 * 60 * 1000, // 1 hour
  TRUST_SCORE_TTL: 6 * 60 * 60 * 1000, // 6 hours
  MARKETPLACE_TTL: 30 * 60 * 1000, // 30 minutes
  IMAGES_TTL: 7 * 24 * 60 * 60 * 1000, // 7 days
  MAX_CACHE_SIZE: 100 * 1024 * 1024, // 100MB
};

// Performance Configuration
export const PERFORMANCE_CONFIG = {
  MAX_IMAGE_SIZE: 2 * 1024 * 1024, // 2MB
  IMAGE_QUALITY: 0.8, // 80%
  MAX_AUDIO_DURATION: 60, // 60 seconds
  LOCATION_TIMEOUT: 10000, // 10 seconds
  LOCATION_CACHE_DURATION: 5 * 60 * 1000, // 5 minutes
};

/**
 * Core type definitions for the Vendor App
 */

// Location
export interface Location {
  latitude: number;
  longitude: number;
}

// Vendor
export interface Vendor {
  id: string;
  username: string;
  name: string;
  phone: string;
  location: Location;
  language: 'en' | 'hi';
  createdAt: string;
}

// Authentication
export interface AuthState {
  vendor: Vendor | null;
  isAuthenticated: boolean;
  token: string | null;
  isDemoMode: boolean;
}

// Transaction
export interface Transaction {
  id: string;
  vendorId: string;
  item: string;
  quantity: number;
  unit: string;
  pricePerUnit: number;
  totalPrice: number;
  timestamp: string;
  source: 'voice' | 'manual';
  audioUrl?: string;
  transcription?: string;
}

// API Response
export interface APIResponse<T> {
  success: boolean;
  data: T;
  error?: {
    code: string;
    message: string;
  };
  timestamp: string;
}

// Environment Variables
export interface EnvConfig {
  API_BASE_URL: string;
  AWS_REGION: string;
  S3_BUCKET_NAME: string;
  FIREBASE_PROJECT_ID: string;
  APP_ENV: 'development' | 'staging' | 'production';
  DEMO_MODE: boolean;
}

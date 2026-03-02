/**
 * Authentication Redux Slice
 */

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import type { Vendor, AuthState } from '../../types';
import { secureStorage } from '../../services/secureStorage';

// Demo credentials
const DEMO_CREDENTIALS = {
  username: 'demo_vendor',
  password: 'hackathon2024',
};

// Demo vendor data
const DEMO_VENDOR: Vendor = {
  id: 'demo_vendor_001',
  username: 'demo_vendor',
  name: 'Demo Vendor',
  phone: '+91 9876543210',
  location: {
    latitude: 28.6139,
    longitude: 77.209,
  },
  language: 'en',
  createdAt: new Date().toISOString(),
};

interface LoginPayload {
  username: string;
  password: string;
  rememberMe: boolean;
  isDemoMode: boolean;
}

interface LoginResponse {
  vendor: Vendor;
  token: string;
  isDemoMode: boolean;
}

// Initial state
const initialState: AuthState = {
  vendor: null,
  isAuthenticated: false,
  token: null,
  isDemoMode: false,
};

/**
 * Login async thunk
 */
export const login = createAsyncThunk<LoginResponse, LoginPayload>(
  'auth/login',
  async ({ username, password, rememberMe, isDemoMode }, { rejectWithValue }) => {
    try {
      // Demo mode login
      if (isDemoMode) {
        if (
          username === DEMO_CREDENTIALS.username &&
          password === DEMO_CREDENTIALS.password
        ) {
          const token = 'demo_token_' + Date.now();
          
          // Store credentials if remember me is checked
          if (rememberMe) {
            await secureStorage.storeCredentials(username, password);
          }
          
          await secureStorage.storeToken(token);

          return {
            vendor: DEMO_VENDOR,
            token,
            isDemoMode: true,
          };
        } else {
          return rejectWithValue('Invalid demo credentials');
        }
      }

      // Production login (to be implemented with actual API)
      // For now, reject non-demo logins
      return rejectWithValue('Production login not yet implemented. Please use demo mode.');
    } catch (error) {
      return rejectWithValue(
        error instanceof Error ? error.message : 'Login failed'
      );
    }
  }
);

/**
 * Logout async thunk
 */
export const logout = createAsyncThunk('auth/logout', async () => {
  await secureStorage.clearAll();
});

/**
 * Auto-login from stored credentials
 */
export const autoLogin = createAsyncThunk('auth/autoLogin', async (_, { rejectWithValue }) => {
  try {
    const credentials = await secureStorage.getCredentials();
    const token = await secureStorage.getToken();

    if (!credentials || !token) {
      return rejectWithValue('No stored credentials');
    }

    // Check if it's demo credentials
    if (
      credentials.username === DEMO_CREDENTIALS.username &&
      credentials.password === DEMO_CREDENTIALS.password
    ) {
      return {
        vendor: DEMO_VENDOR,
        token,
        isDemoMode: true,
      };
    }

    // For production, validate token with backend
    return rejectWithValue('Auto-login not available for production accounts');
  } catch (error) {
    return rejectWithValue(
      error instanceof Error ? error.message : 'Auto-login failed'
    );
  }
});

// Auth slice
const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    clearError: (state) => {
      // Clear any error state if needed
    },
  },
  extraReducers: (builder) => {
    builder
      // Login
      .addCase(login.fulfilled, (state, action: PayloadAction<LoginResponse>) => {
        state.vendor = action.payload.vendor;
        state.token = action.payload.token;
        state.isAuthenticated = true;
        state.isDemoMode = action.payload.isDemoMode;
      })
      .addCase(login.rejected, (state) => {
        state.vendor = null;
        state.token = null;
        state.isAuthenticated = false;
        state.isDemoMode = false;
      })
      // Logout
      .addCase(logout.fulfilled, (state) => {
        state.vendor = null;
        state.token = null;
        state.isAuthenticated = false;
        state.isDemoMode = false;
      })
      // Auto-login
      .addCase(autoLogin.fulfilled, (state, action: PayloadAction<LoginResponse>) => {
        state.vendor = action.payload.vendor;
        state.token = action.payload.token;
        state.isAuthenticated = true;
        state.isDemoMode = action.payload.isDemoMode;
      })
      .addCase(autoLogin.rejected, (state) => {
        state.vendor = null;
        state.token = null;
        state.isAuthenticated = false;
        state.isDemoMode = false;
      });
  },
});

export const { clearError } = authSlice.actions;
export default authSlice.reducer;

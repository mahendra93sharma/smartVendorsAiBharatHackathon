/**
 * Secure Storage Service
 * Provides secure credential storage using AsyncStorage with basic encoding
 * 
 * Note: For production, consider using:
 * - iOS: react-native-keychain (Keychain Services)
 * - Android: react-native-encrypted-storage (EncryptedSharedPreferences)
 */

import AsyncStorage from '@react-native-async-storage/async-storage';

const STORAGE_KEYS = {
  USERNAME: '@vendor_app:username',
  PASSWORD: '@vendor_app:password',
  TOKEN: '@vendor_app:token',
  REMEMBER_ME: '@vendor_app:remember_me',
};

// Simple encoding for basic obfuscation
// In production, use proper encryption libraries
const encode = (value: string): string => {
  // Simple character code shift for obfuscation
  return value
    .split('')
    .map((char) => String.fromCharCode(char.charCodeAt(0) + 7))
    .join('');
};

const decode = (value: string): string => {
  // Reverse the character code shift
  return value
    .split('')
    .map((char) => String.fromCharCode(char.charCodeAt(0) - 7))
    .join('');
};

export const secureStorage = {
  /**
   * Store credentials securely
   */
  async storeCredentials(username: string, password: string): Promise<void> {
    try {
      await AsyncStorage.multiSet([
        [STORAGE_KEYS.USERNAME, encode(username)],
        [STORAGE_KEYS.PASSWORD, encode(password)],
        [STORAGE_KEYS.REMEMBER_ME, 'true'],
      ]);
    } catch (error) {
      console.error('Error storing credentials:', error);
      throw error;
    }
  },

  /**
   * Retrieve stored credentials
   */
  async getCredentials(): Promise<{ username: string; password: string } | null> {
    try {
      const rememberMe = await AsyncStorage.getItem(STORAGE_KEYS.REMEMBER_ME);
      if (rememberMe !== 'true') {
        return null;
      }

      const values = await AsyncStorage.multiGet([
        STORAGE_KEYS.USERNAME,
        STORAGE_KEYS.PASSWORD,
      ]);

      const username = values[0][1];
      const password = values[1][1];

      if (!username || !password) {
        return null;
      }

      return {
        username: decode(username),
        password: decode(password),
      };
    } catch (error) {
      console.error('Error retrieving credentials:', error);
      return null;
    }
  },

  /**
   * Clear stored credentials
   */
  async clearCredentials(): Promise<void> {
    try {
      await AsyncStorage.multiRemove([
        STORAGE_KEYS.USERNAME,
        STORAGE_KEYS.PASSWORD,
        STORAGE_KEYS.REMEMBER_ME,
      ]);
    } catch (error) {
      console.error('Error clearing credentials:', error);
      throw error;
    }
  },

  /**
   * Store authentication token
   */
  async storeToken(token: string): Promise<void> {
    try {
      await AsyncStorage.setItem(STORAGE_KEYS.TOKEN, token);
    } catch (error) {
      console.error('Error storing token:', error);
      throw error;
    }
  },

  /**
   * Retrieve authentication token
   */
  async getToken(): Promise<string | null> {
    try {
      return await AsyncStorage.getItem(STORAGE_KEYS.TOKEN);
    } catch (error) {
      console.error('Error retrieving token:', error);
      return null;
    }
  },

  /**
   * Clear authentication token
   */
  async clearToken(): Promise<void> {
    try {
      await AsyncStorage.removeItem(STORAGE_KEYS.TOKEN);
    } catch (error) {
      console.error('Error clearing token:', error);
      throw error;
    }
  },

  /**
   * Clear all secure data
   */
  async clearAll(): Promise<void> {
    try {
      await AsyncStorage.multiRemove([
        STORAGE_KEYS.USERNAME,
        STORAGE_KEYS.PASSWORD,
        STORAGE_KEYS.TOKEN,
        STORAGE_KEYS.REMEMBER_ME,
      ]);
    } catch (error) {
      console.error('Error clearing all secure data:', error);
      throw error;
    }
  },
};

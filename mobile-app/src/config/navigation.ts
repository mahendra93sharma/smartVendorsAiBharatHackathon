/**
 * Navigation Configuration
 * Centralized configuration for navigation behavior and styling
 */

import { Platform } from 'react-native';

export const navigationConfig = {
  // Screen transition animations
  animations: {
    default: 'slide_from_right' as const,
    modal: 'fade' as const,
    none: 'none' as const,
  },

  // Tab bar configuration
  tabBar: {
    height: Platform.OS === 'ios' ? 88 : 64,
    paddingBottom: Platform.OS === 'ios' ? 24 : 8,
    paddingTop: 8,
    activeTintColor: '#4CAF50',
    inactiveTintColor: '#757575',
    labelStyle: {
      fontSize: 12,
      fontWeight: '600' as const,
    },
  },

  // Header configuration
  header: {
    backgroundColor: '#ffffff',
    tintColor: '#333333',
    titleStyle: {
      fontSize: 18,
      fontWeight: '600' as const,
    },
  },

  // Deep linking prefixes
  linking: {
    prefixes: ['vendorapp://', 'https://vendorapp.com'],
  },
};

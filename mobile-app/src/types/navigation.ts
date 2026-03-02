/**
 * Navigation Types
 * TypeScript type definitions for React Navigation
 */

import type { NavigatorScreenParams } from '@react-navigation/native';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import type { BottomTabScreenProps } from '@react-navigation/bottom-tabs';

// Root Stack Navigator (Auth + Main)
export type RootStackParamList = {
  Auth: NavigatorScreenParams<AuthStackParamList>;
  Main: NavigatorScreenParams<MainTabParamList>;
};

// Auth Stack Navigator
export type AuthStackParamList = {
  Login: undefined;
  Onboarding: undefined;
};

// Main Tab Navigator
export type MainTabParamList = {
  HomeTab: NavigatorScreenParams<HomeStackParamList>;
  PricesTab: NavigatorScreenParams<PricesStackParamList>;
  ScannerTab: NavigatorScreenParams<ScannerStackParamList>;
  MarketplaceTab: NavigatorScreenParams<MarketplaceStackParamList>;
  ProfileTab: NavigatorScreenParams<ProfileStackParamList>;
};

// Home Stack Navigator
export type HomeStackParamList = {
  Home: undefined;
  VoiceTransaction: undefined;
  TransactionDetail: { transactionId: string };
  TransactionHistory: undefined;
};

// Prices Stack Navigator
export type PricesStackParamList = {
  PriceSearch: undefined;
  PriceComparison: { item: string };
};

// Scanner Stack Navigator
export type ScannerStackParamList = {
  Camera: undefined;
  ClassificationResult: {
    category: 'Fresh' | 'B-Grade' | 'Waste';
    confidence: number;
    imageUrl: string;
    shelfLife?: number;
    suggestions: string[];
  };
};

// Marketplace Stack Navigator
export type MarketplaceStackParamList = {
  Listings: undefined;
  ListingDetail: { listingId: string };
  CreateListing: { prefilledItem?: string };
};

// Profile Stack Navigator
export type ProfileStackParamList = {
  TrustScore: undefined;
  Settings: undefined;
  About: undefined;
};

// Screen Props Types
export type RootStackScreenProps<T extends keyof RootStackParamList> =
  NativeStackScreenProps<RootStackParamList, T>;

export type AuthStackScreenProps<T extends keyof AuthStackParamList> =
  NativeStackScreenProps<AuthStackParamList, T>;

export type MainTabScreenProps<T extends keyof MainTabParamList> =
  BottomTabScreenProps<MainTabParamList, T>;

export type HomeStackScreenProps<T extends keyof HomeStackParamList> =
  NativeStackScreenProps<HomeStackParamList, T>;

export type PricesStackScreenProps<T extends keyof PricesStackParamList> =
  NativeStackScreenProps<PricesStackParamList, T>;

export type ScannerStackScreenProps<T extends keyof ScannerStackParamList> =
  NativeStackScreenProps<ScannerStackParamList, T>;

export type MarketplaceStackScreenProps<T extends keyof MarketplaceStackParamList> =
  NativeStackScreenProps<MarketplaceStackParamList, T>;

export type ProfileStackScreenProps<T extends keyof ProfileStackParamList> =
  NativeStackScreenProps<ProfileStackParamList, T>;

// Deep Linking Configuration
export const linking = {
  prefixes: ['vendorapp://', 'https://vendorapp.com'],
  config: {
    screens: {
      Auth: {
        screens: {
          Login: 'login',
          Onboarding: 'onboarding',
        },
      },
      Main: {
        screens: {
          HomeTab: {
            screens: {
              Home: 'home',
              VoiceTransaction: 'voice-transaction',
              TransactionDetail: 'transaction/:transactionId',
              TransactionHistory: 'transactions',
            },
          },
          PricesTab: {
            screens: {
              PriceSearch: 'prices',
              PriceComparison: 'prices/:item',
            },
          },
          ScannerTab: {
            screens: {
              Camera: 'scanner',
              ClassificationResult: 'scanner/result',
            },
          },
          MarketplaceTab: {
            screens: {
              Listings: 'marketplace',
              ListingDetail: 'marketplace/:listingId',
              CreateListing: 'marketplace/create',
            },
          },
          ProfileTab: {
            screens: {
              TrustScore: 'profile',
              Settings: 'settings',
              About: 'about',
            },
          },
        },
      },
    },
  },
};

declare global {
  namespace ReactNavigation {
    interface RootParamList extends RootStackParamList {}
  }
}

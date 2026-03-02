# Navigation Structure

This directory contains the navigation configuration for the Vendor App mobile application.

## Architecture

The navigation follows a hierarchical structure:

```
RootNavigator (Root Stack)
├── Auth (Auth Stack) - When not authenticated
│   └── Login
└── Main (Bottom Tabs) - When authenticated
    ├── HomeTab (Stack)
    │   ├── Home
    │   ├── VoiceTransaction
    │   ├── TransactionDetail
    │   └── TransactionHistory
    ├── PricesTab (Stack)
    │   ├── PriceSearch
    │   └── PriceComparison
    ├── ScannerTab (Stack)
    │   ├── Camera
    │   └── ClassificationResult
    ├── MarketplaceTab (Stack)
    │   ├── Listings
    │   ├── ListingDetail
    │   └── CreateListing
    └── ProfileTab (Stack)
        ├── TrustScore
        ├── Settings
        └── About
```

## Components

### AppNavigator
The main navigation container that wraps the entire app with `NavigationContainer` and configures deep linking.

### RootNavigator
The root stack navigator that switches between Auth and Main stacks based on authentication state.

### AuthStackNavigator
Handles authentication-related screens (Login, Onboarding).

### MainTabNavigator
The bottom tab navigator with 5 tabs: Home, Prices, Scanner, Marketplace, and Profile.

### Stack Navigators
Each tab has its own stack navigator:
- **HomeStackNavigator**: Home dashboard and transaction screens
- **PricesStackNavigator**: Price search and comparison screens
- **ScannerStackNavigator**: Camera and classification result screens
- **MarketplaceStackNavigator**: Marketplace listings and creation screens
- **ProfileStackNavigator**: Trust score, settings, and about screens

## Deep Linking

The app supports deep linking with the following URL schemes:
- `vendorapp://` - Custom URL scheme
- `https://vendorapp.com` - Universal links

### Example Deep Links
- `vendorapp://home` - Navigate to home screen
- `vendorapp://transaction/123` - Navigate to specific transaction
- `vendorapp://prices/tomato` - Navigate to tomato price comparison
- `vendorapp://marketplace/create` - Navigate to create listing screen

## Navigation Guards

The `RootNavigator` implements authentication guards:
- Unauthenticated users see the Auth stack (Login screen)
- Authenticated users see the Main stack (Bottom tabs)

## TypeScript Types

All navigation types are defined in `src/types/navigation.ts`:
- Route parameter types for each screen
- Screen props types for type-safe navigation
- Deep linking configuration

## Usage

### Navigating Between Screens

```typescript
import { useNavigation } from '@react-navigation/native';
import type { HomeStackScreenProps } from '../../types/navigation';

const MyScreen: React.FC<HomeStackScreenProps<'Home'>> = ({ navigation }) => {
  // Navigate to another screen
  navigation.navigate('VoiceTransaction');
  
  // Navigate with parameters
  navigation.navigate('TransactionDetail', { transactionId: '123' });
  
  // Go back
  navigation.goBack();
};
```

### Accessing Route Parameters

```typescript
import { useRoute } from '@react-navigation/native';
import type { HomeStackScreenProps } from '../../types/navigation';

const MyScreen: React.FC<HomeStackScreenProps<'TransactionDetail'>> = ({ route }) => {
  const { transactionId } = route.params;
  // Use transactionId
};
```

## Screen Transitions

Default transitions:
- **Stack screens**: Slide from right (iOS/Android standard)
- **Auth screens**: Fade animation
- **Tab switches**: No animation (instant)

## Customization

Navigation configuration can be customized in `src/config/navigation.ts`:
- Tab bar styling
- Header styling
- Animation types
- Deep linking prefixes

## Future Enhancements

- [ ] Add modal screens for forms
- [ ] Implement navigation state persistence
- [ ] Add screen tracking for analytics
- [ ] Implement navigation guards for permissions
- [ ] Add gesture-based navigation

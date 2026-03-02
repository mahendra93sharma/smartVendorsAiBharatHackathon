# Project Structure

This document describes the organization of the Vendor App mobile application.

## Directory Structure

```
mobile-app/
├── android/                    # Android native code
│   ├── app/
│   │   ├── src/main/
│   │   │   ├── AndroidManifest.xml
│   │   │   └── res/
│   │   ├── build.gradle
│   │   └── proguard-rules.pro
│   ├── build.gradle
│   ├── gradle.properties
│   └── settings.gradle
│
├── ios/                        # iOS native code
│   ├── VendorApp/
│   │   └── Info.plist
│   └── Podfile
│
├── src/                        # Application source code
│   ├── components/             # Reusable UI components
│   │   ├── common/            # Common components (Button, Card, Input)
│   │   └── navigation/        # Navigation components
│   │
│   ├── screens/               # Screen components
│   │   ├── Home/
│   │   ├── VoiceTransaction/
│   │   ├── Prices/
│   │   ├── Scanner/
│   │   ├── Marketplace/
│   │   └── TrustScore/
│   │
│   ├── services/              # API and service integrations
│   │   ├── api.ts            # API client
│   │   ├── s3.ts             # S3 upload service
│   │   ├── cache.ts          # Cache management
│   │   ├── offlineQueue.ts   # Offline operation queue
│   │   ├── permissions.ts    # Permission handling
│   │   ├── location.ts       # Geolocation service
│   │   └── notifications.ts  # Push notifications
│   │
│   ├── store/                 # Redux state management
│   │   ├── index.ts          # Store configuration
│   │   └── slices/           # Redux slices
│   │       ├── authSlice.ts
│   │       ├── transactionsSlice.ts
│   │       ├── pricesSlice.ts
│   │       ├── marketplaceSlice.ts
│   │       ├── trustScoreSlice.ts
│   │       └── uiSlice.ts
│   │
│   ├── utils/                 # Utility functions
│   │   ├── index.ts          # Common utilities
│   │   ├── compression.ts    # Image compression
│   │   ├── validation.ts     # Form validation
│   │   ├── formatting.ts     # Data formatting
│   │   └── distance.ts       # Distance calculations
│   │
│   ├── types/                 # TypeScript type definitions
│   │   ├── index.ts          # Core types
│   │   ├── api.ts            # API types
│   │   ├── models.ts         # Data models
│   │   └── navigation.ts     # Navigation types
│   │
│   ├── hooks/                 # Custom React hooks
│   │   ├── useOffline.ts     # Offline detection
│   │   ├── usePermissions.ts # Permission management
│   │   └── useLocation.ts    # Location access
│   │
│   ├── locales/              # Internationalization
│   │   ├── en/              # English translations
│   │   └── hi/              # Hindi translations
│   │
│   ├── mocks/                # Mock data for demo mode
│   │   └── data.json
│   │
│   └── config/               # App configuration
│       ├── env.ts           # Environment variables
│       ├── aws.ts           # AWS configuration
│       ├── navigation.ts    # Navigation config
│       └── theme.ts         # Theme configuration
│
├── __tests__/                # Test files
│   ├── unit/                # Unit tests
│   ├── property/            # Property-based tests
│   ├── integration/         # Integration tests
│   └── e2e/                 # End-to-end tests
│
├── .env.example              # Environment variables template
├── .eslintrc.js             # ESLint configuration
├── .prettierrc.js           # Prettier configuration
├── .gitignore               # Git ignore rules
├── .watchmanconfig          # Watchman configuration
├── app.json                 # App metadata
├── App.tsx                  # Root component
├── babel.config.js          # Babel configuration
├── index.js                 # Entry point
├── jest.config.js           # Jest configuration
├── metro.config.js          # Metro bundler config
├── package.json             # Dependencies and scripts
├── tsconfig.json            # TypeScript configuration
└── README.md                # Project documentation
```

## Key Directories

### `/src/components`
Reusable UI components organized by type:
- `common/`: Basic UI elements (Button, Card, Input, Badge)
- `navigation/`: Navigation-related components

### `/src/screens`
Screen-level components, one directory per feature:
- Each screen has its own directory with components and styles
- Follows feature-based organization

### `/src/services`
Business logic and external service integrations:
- API client with interceptors
- AWS service wrappers (S3, etc.)
- Cache management
- Offline queue
- Native module wrappers (camera, location, etc.)

### `/src/store`
Redux state management:
- Store configuration with Redux Toolkit
- Slices for each feature domain
- Async thunks for side effects
- Redux Persist configuration

### `/src/utils`
Pure utility functions:
- Data formatting
- Validation
- Calculations
- Helper functions

### `/src/types`
TypeScript type definitions:
- Shared types and interfaces
- API contracts
- Data models
- Navigation types

### `/src/hooks`
Custom React hooks:
- Reusable stateful logic
- Native module access
- Common patterns

### `/src/locales`
Internationalization files:
- Translation files for each language
- Organized by feature/screen

### `/src/config`
Application configuration:
- Environment variables
- Constants
- Theme configuration
- Service configurations

## Naming Conventions

### Files
- Components: PascalCase (e.g., `HomeScreen.tsx`, `Button.tsx`)
- Services: camelCase (e.g., `apiService.ts`, `cacheService.ts`)
- Utilities: camelCase (e.g., `compression.ts`, `validation.ts`)
- Types: camelCase (e.g., `api.ts`, `models.ts`)

### Variables
- camelCase for variables and functions
- PascalCase for components and classes
- UPPER_SNAKE_CASE for constants

### Imports
Use path aliases for cleaner imports:
```typescript
import { Button } from '@components/common/Button';
import { apiService } from '@services/api';
import { useAuth } from '@hooks/useAuth';
```

## Code Organization Principles

1. **Feature-based structure**: Group related files by feature
2. **Separation of concerns**: UI, business logic, and state are separate
3. **Reusability**: Common components and utilities are shared
4. **Type safety**: TypeScript throughout with strict mode
5. **Testability**: Easy to test with clear dependencies
6. **Scalability**: Structure supports growth without reorganization

## Adding New Features

When adding a new feature:

1. Create screen directory in `/src/screens/[FeatureName]`
2. Add Redux slice in `/src/store/slices/[featureName]Slice.ts`
3. Create service if needed in `/src/services/[featureName].ts`
4. Add types in `/src/types/[featureName].ts`
5. Create tests in `__tests__/unit/[featureName]/`
6. Add translations in `/src/locales/[lang]/[featureName].json`

## Best Practices

- Keep components small and focused
- Use TypeScript strict mode
- Write tests alongside code
- Document complex logic
- Follow React Native best practices
- Use hooks for stateful logic
- Memoize expensive computations
- Optimize list rendering
- Handle errors gracefully
- Support offline mode

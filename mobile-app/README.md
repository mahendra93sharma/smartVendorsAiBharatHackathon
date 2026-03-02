# Vendor App - React Native Mobile Application

A native mobile application for Android and iOS built with React Native CLI, connecting to AWS backend infrastructure for street vendors in India.

## Features

- 🎤 Voice transaction recording with Hindi transcription
- 💰 Market price intelligence from multiple mandis
- 📸 Produce freshness scanning with AI classification
- 🛒 B-Grade produce marketplace
- 🏆 Trust Score and vendor reputation system
- 📱 Offline-first architecture with data sync
- 🌐 Multi-language support (Hindi & English)
- 🔔 Push notifications for marketplace activity

## Prerequisites

### General Requirements
- Node.js >= 18
- npm >= 9 or yarn >= 1.22
- Git
- React Native CLI
- TypeScript

### Android Development
- Android Studio
- Android SDK (API 21-33)
- Java JDK 11
- Android Emulator or physical device

### iOS Development (macOS only)
- Xcode 14+
- CocoaPods
- iOS Simulator or physical device
- Apple Developer account (for device testing)

## Project Structure

```
mobile-app/
├── src/
│   ├── screens/          # Screen components
│   ├── components/       # Reusable UI components
│   ├── services/         # API and AWS service integrations
│   ├── store/            # Redux state management
│   ├── utils/            # Utility functions
│   ├── types/            # TypeScript type definitions
│   ├── hooks/            # Custom React hooks
│   ├── locales/          # i18n translation files
│   ├── mocks/            # Mock data for demo mode
│   └── config/           # App configuration
├── android/              # Android native code
├── ios/                  # iOS native code
├── __tests__/            # Test files
└── ...config files
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mobile-app
```

2. Install dependencies:
```bash
npm install
```

3. Install iOS dependencies (macOS only):
```bash
cd ios && pod install && cd ..
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
API_BASE_URL=https://your-api-gateway-url.com
AWS_REGION=ap-south-1
S3_BUCKET_NAME=your-s3-bucket-name
FIREBASE_PROJECT_ID=your-firebase-project-id
```

### TypeScript Configuration

The project uses TypeScript with strict mode enabled. Path aliases are configured for cleaner imports:

```typescript
import { Button } from '@components/common/Button';
import { apiService } from '@services/api';
import { useAuth } from '@hooks/useAuth';
```

## Running the App

### Development Mode

**Android:**
```bash
npm run android
```

**iOS:**
```bash
npm run ios
```

**Start Metro Bundler:**
```bash
npm start
```

### Production Build

**Android APK:**
```bash
npm run build:android
```

**iOS Archive:**
```bash
npm run build:ios
```

## Testing

### Run all tests:
```bash
npm test
```

### Run tests in watch mode:
```bash
npm run test:watch
```

### Generate coverage report:
```bash
npm run test:coverage
```

## Code Quality

### Linting:
```bash
npm run lint
```

### Formatting:
```bash
npm run format
```

## Architecture

### State Management
- Redux Toolkit for global state
- Redux Persist for state persistence
- AsyncStorage for local data

### Navigation
- React Navigation v6
- Bottom tab navigator
- Stack navigators for each feature

### Offline Support
- Offline-first architecture
- Request queueing when offline
- Automatic sync when connection restored
- Cached data with TTL

### AWS Integration
- S3 for file uploads (audio, images)
- API Gateway for backend communication
- AWS Amplify for service integration

## Performance Optimization

- Hermes engine enabled (Android)
- Image compression before upload
- List virtualization with FlatList
- Lazy loading for screens
- Optimized for 2GB RAM devices

## Platform Support

- **Android:** API 21+ (Android 5.0+)
- **iOS:** iOS 12.0+
- **Devices:** Optimized for 2GB RAM minimum

## Troubleshooting

### Android Build Issues

1. Clean build:
```bash
cd android && ./gradlew clean && cd ..
```

2. Reset Metro cache:
```bash
npm start -- --reset-cache
```

### iOS Build Issues

1. Clean build folder:
```bash
cd ios && xcodebuild clean && cd ..
```

2. Reinstall pods:
```bash
cd ios && pod deintegrate && pod install && cd ..
```

### Common Issues

**Metro bundler not starting:**
```bash
npx react-native start --reset-cache
```

**Native module linking issues:**
```bash
npm install
cd ios && pod install && cd ..
```

## Contributing

1. Follow TypeScript strict mode guidelines
2. Write tests for new features
3. Run linter before committing
4. Follow React Native best practices
5. Update documentation for new features

## License

[Your License Here]

## Support

For issues and questions, please refer to the project documentation or contact the development team.

# Getting Started: React Native Mobile App Development

## Quick Overview

This guide will help you set up your development environment and start building the Smart Vendors mobile app for Android and iOS.

## Prerequisites

### Required for All Platforms
- **Node.js**: 16.x or higher ([Download](https://nodejs.org/))
- **npm** or **yarn**: Package manager
- **Git**: Version control
- **React Native CLI**: `npm install -g react-native-cli`
- **Code Editor**: VS Code recommended

### Required for Android Development
- **Android Studio**: Latest version ([Download](https://developer.android.com/studio))
- **Android SDK**: API Level 21-33
- **Java JDK**: Version 11 ([Download](https://www.oracle.com/java/technologies/downloads/))
- **Android Emulator** or physical Android device

### Required for iOS Development (macOS only)
- **Xcode**: 14.x or higher ([Mac App Store](https://apps.apple.com/us/app/xcode/id497799835))
- **CocoaPods**: `sudo gem install cocoapods`
- **iOS Simulator** or physical iOS device
- **Apple Developer Account**: For device testing and App Store

## Environment Setup

### 1. Install Node.js and npm
```bash
# Check if installed
node --version  # Should be 16.x or higher
npm --version

# If not installed, download from https://nodejs.org/
```

### 2. Install React Native CLI
```bash
npm install -g react-native-cli
```

### 3. Set Up Android Development Environment

#### Install Android Studio
1. Download from https://developer.android.com/studio
2. Install with default settings
3. Open Android Studio
4. Go to **Tools → SDK Manager**
5. Install:
   - Android SDK Platform 33 (Android 13)
   - Android SDK Platform 21 (Android 5.0)
   - Android SDK Build-Tools
   - Android Emulator
   - Android SDK Platform-Tools

#### Configure Environment Variables
Add to your `~/.zshrc` or `~/.bash_profile`:
```bash
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/tools/bin
```

Reload:
```bash
source ~/.zshrc  # or source ~/.bash_profile
```

#### Install Java JDK 11
```bash
# macOS with Homebrew
brew install openjdk@11

# Verify installation
java -version
```

#### Create Android Emulator
1. Open Android Studio
2. Go to **Tools → AVD Manager**
3. Click **Create Virtual Device**
4. Select **Pixel 4** (or any phone)
5. Select **API Level 33** (Android 13)
6. Click **Finish**

### 4. Set Up iOS Development Environment (macOS only)

#### Install Xcode
1. Download from Mac App Store
2. Install (this takes a while)
3. Open Xcode
4. Go to **Preferences → Locations**
5. Select Command Line Tools version

#### Install CocoaPods
```bash
sudo gem install cocoapods
```

#### Install iOS Simulator
1. Open Xcode
2. Go to **Xcode → Preferences → Components**
3. Download iOS simulators you need

## Project Initialization

### 1. Create New React Native Project
```bash
# Navigate to your workspace
cd /path/to/your/workspace

# Create new React Native project with TypeScript
npx react-native init SmartVendorsMobile --template react-native-template-typescript

# Navigate to project
cd SmartVendorsMobile
```

### 2. Project Structure
```
SmartVendorsMobile/
├── android/              # Android native code
├── ios/                  # iOS native code
├── src/                  # Source code
│   ├── screens/         # Screen components
│   ├── components/      # Reusable components
│   ├── services/        # API and AWS services
│   ├── store/           # Redux store
│   ├── navigation/      # Navigation configuration
│   ├── utils/           # Utility functions
│   ├── types/           # TypeScript types
│   └── assets/          # Images, fonts, etc.
├── App.tsx              # Root component
├── package.json         # Dependencies
└── tsconfig.json        # TypeScript config
```

### 3. Install Core Dependencies
```bash
# Navigation
npm install @react-navigation/native @react-navigation/native-stack @react-navigation/bottom-tabs
npm install react-native-screens react-native-safe-area-context

# State Management
npm install @reduxjs/toolkit react-redux redux-persist

# AWS Integration
npm install aws-amplify @aws-amplify/react-native axios

# Storage
npm install @react-native-async-storage/async-storage

# Native Modules
npm install react-native-voice
npm install react-native-camera
npm install @react-native-community/geolocation
npm install react-native-vector-icons
npm install react-native-gesture-handler

# Utilities
npm install react-native-config
npm install @react-native-community/netinfo
npm install react-native-fast-image

# Development
npm install --save-dev @types/react @types/react-native
```

### 4. Link Native Dependencies

#### iOS
```bash
cd ios
pod install
cd ..
```

#### Android
Most dependencies auto-link, but verify in `android/app/build.gradle`

### 5. Configure Environment Variables
Create `.env` file:
```bash
API_BASE_URL=https://your-api-gateway-url.amazonaws.com
AWS_REGION=ap-south-1
S3_BUCKET_NAME=smart-vendors-frontend-1772474994
DEMO_MODE=false
```

Create `.env.example`:
```bash
API_BASE_URL=
AWS_REGION=
S3_BUCKET_NAME=
DEMO_MODE=
```

## Running the App

### Run on Android

#### Start Metro Bundler
```bash
npm start
```

#### Run on Android Emulator (in new terminal)
```bash
# Start emulator first (or connect physical device)
npm run android
```

#### Run on Physical Android Device
1. Enable Developer Options on device
2. Enable USB Debugging
3. Connect device via USB
4. Run: `npm run android`

### Run on iOS

#### Start Metro Bundler
```bash
npm start
```

#### Run on iOS Simulator (in new terminal)
```bash
npm run ios
```

#### Run on Physical iOS Device
1. Open `ios/SmartVendorsMobile.xcworkspace` in Xcode
2. Select your device
3. Click Run (▶️)

## Development Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/voice-transaction
```

### 2. Implement Feature
Follow the task list in `tasks.md`

### 3. Test Locally
```bash
# Run tests
npm test

# Run linter
npm run lint

# Format code
npm run format
```

### 4. Build for Testing

#### Android Debug APK
```bash
cd android
./gradlew assembleDebug
# APK location: android/app/build/outputs/apk/debug/app-debug.apk
```

#### iOS Debug Build
1. Open Xcode
2. Select **Generic iOS Device**
3. Product → Archive
4. Distribute App → Development

## Connecting to AWS Backend

### 1. Configure AWS Amplify
```typescript
// src/services/aws-config.ts
import { Amplify } from 'aws-amplify';

Amplify.configure({
  API: {
    endpoints: [
      {
        name: 'SmartVendorsAPI',
        endpoint: process.env.API_BASE_URL,
        region: process.env.AWS_REGION,
      },
    ],
  },
  Storage: {
    AWSS3: {
      bucket: process.env.S3_BUCKET_NAME,
      region: process.env.AWS_REGION,
    },
  },
});
```

### 2. Create API Service
```typescript
// src/services/api.ts
import axios from 'axios';
import Config from 'react-native-config';

const api = axios.create({
  baseURL: Config.API_BASE_URL,
  timeout: 30000,
});

// Add interceptors
api.interceptors.response.use(
  response => response,
  error => {
    // Handle errors
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export default api;
```

### 3. Test API Connection
```typescript
// Test in App.tsx
import api from './src/services/api';

useEffect(() => {
  api.get('/health')
    .then(response => console.log('API Connected:', response.data))
    .catch(error => console.error('API Error:', error));
}, []);
```

## Common Issues and Solutions

### Android Issues

#### Issue: "SDK location not found"
**Solution:**
```bash
# Create local.properties in android/
echo "sdk.dir=/Users/YOUR_USERNAME/Library/Android/sdk" > android/local.properties
```

#### Issue: "Execution failed for task ':app:installDebug'"
**Solution:**
```bash
cd android
./gradlew clean
cd ..
npm run android
```

#### Issue: Metro bundler port conflict
**Solution:**
```bash
# Kill process on port 8081
lsof -ti:8081 | xargs kill -9
npm start
```

### iOS Issues

#### Issue: "CocoaPods not installed"
**Solution:**
```bash
sudo gem install cocoapods
cd ios
pod install
```

#### Issue: "No bundle URL present"
**Solution:**
```bash
# Clean build
cd ios
rm -rf Pods Podfile.lock
pod install
cd ..
npm start -- --reset-cache
```

#### Issue: "Command PhaseScriptExecution failed"
**Solution:**
```bash
cd ios
pod deintegrate
pod install
```

## Testing on Physical Devices

### Android Physical Device
1. Enable Developer Options:
   - Go to Settings → About Phone
   - Tap Build Number 7 times
2. Enable USB Debugging:
   - Settings → Developer Options → USB Debugging
3. Connect via USB
4. Run: `npm run android`

### iOS Physical Device
1. Connect iPhone via USB
2. Open Xcode
3. Select your device
4. Trust computer on device
5. Click Run

## Next Steps

1. ✅ Environment set up
2. ✅ Project initialized
3. ✅ Dependencies installed
4. ✅ App running on emulator/simulator
5. 📋 Start implementing features from `tasks.md`
6. 🧪 Write tests as you go
7. 📱 Test on physical devices regularly
8. 🚀 Build and release

## Useful Commands

```bash
# Start Metro bundler
npm start

# Run on Android
npm run android

# Run on iOS
npm run ios

# Run tests
npm test

# Run linter
npm run lint

# Format code
npm run format

# Clean Android build
cd android && ./gradlew clean && cd ..

# Clean iOS build
cd ios && rm -rf Pods Podfile.lock && pod install && cd ..

# Reset Metro cache
npm start -- --reset-cache

# Generate Android release APK
cd android && ./gradlew assembleRelease && cd ..

# Generate Android release AAB
cd android && ./gradlew bundleRelease && cd ..
```

## Resources

### Official Documentation
- [React Native Docs](https://reactnative.dev/docs/getting-started)
- [React Navigation](https://reactnavigation.org/docs/getting-started)
- [Redux Toolkit](https://redux-toolkit.js.org/)
- [AWS Amplify](https://docs.amplify.aws/)

### Android Resources
- [Android Developer Guide](https://developer.android.com/guide)
- [Material Design](https://material.io/design)

### iOS Resources
- [iOS Developer Guide](https://developer.apple.com/documentation/)
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)

### Community
- [React Native Community](https://github.com/react-native-community)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/react-native)
- [Reddit r/reactnative](https://www.reddit.com/r/reactnative/)

## Support

If you encounter issues:
1. Check this guide's troubleshooting section
2. Search React Native documentation
3. Check GitHub issues for the specific package
4. Ask in React Native community forums

---

**Ready to start building!** 🚀

Follow the tasks in `tasks.md` to implement each feature step by step.

# Setup Guide - Vendor App

Complete setup instructions for the React Native mobile application.

## Prerequisites

Before you begin, ensure you have the following installed:

### Required for All Platforms
- **Node.js** (v18 or higher): [Download](https://nodejs.org/)
- **npm** (v9 or higher) or **yarn** (v1.22 or higher)
- **Git**: [Download](https://git-scm.com/)
- **React Native CLI**: Install globally with `npm install -g react-native-cli`
- **Watchman** (recommended): [Installation Guide](https://facebook.github.io/watchman/docs/install)

### For Android Development
- **Android Studio**: [Download](https://developer.android.com/studio)
- **Android SDK** (API 21-33)
- **Java JDK 11**: [Download](https://www.oracle.com/java/technologies/javase/jdk11-archive-downloads.html)
- **Android Emulator** or physical Android device

### For iOS Development (macOS only)
- **Xcode 14+**: Install from Mac App Store
- **CocoaPods**: Install with `sudo gem install cocoapods`
- **iOS Simulator** or physical iOS device
- **Apple Developer Account** (for device testing and App Store submission)

## Step 1: Clone and Install

```bash
# Clone the repository
git clone <repository-url>
cd mobile-app

# Install dependencies
npm install

# For iOS, install CocoaPods dependencies
cd ios && pod install && cd ..
```

## Step 2: Environment Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your configuration:
```env
API_BASE_URL=https://your-api-gateway-url.com
AWS_REGION=ap-south-1
S3_BUCKET_NAME=your-s3-bucket-name
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
FIREBASE_PROJECT_ID=your-firebase-project
FIREBASE_API_KEY=your_firebase_api_key
APP_ENV=development
DEMO_MODE=false
```

## Step 3: Android Setup

### Install Android Studio

1. Download and install [Android Studio](https://developer.android.com/studio)
2. During installation, ensure these components are selected:
   - Android SDK
   - Android SDK Platform
   - Android Virtual Device

### Configure Android SDK

1. Open Android Studio
2. Go to **Preferences** → **Appearance & Behavior** → **System Settings** → **Android SDK**
3. Select **SDK Platforms** tab and install:
   - Android 13.0 (API 33)
   - Android 5.0 (API 21)
4. Select **SDK Tools** tab and install:
   - Android SDK Build-Tools
   - Android Emulator
   - Android SDK Platform-Tools

### Set Environment Variables

Add to your `~/.bash_profile` or `~/.zshrc`:

```bash
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/tools/bin
```

Reload your shell:
```bash
source ~/.bash_profile  # or source ~/.zshrc
```

### Create Android Virtual Device (AVD)

1. Open Android Studio
2. Go to **Tools** → **AVD Manager**
3. Click **Create Virtual Device**
4. Select a device (e.g., Pixel 4)
5. Select system image (API 33 recommended)
6. Click **Finish**

### Run on Android

```bash
# Start Metro bundler
npm start

# In another terminal, run on Android
npm run android

# Or run on specific device
npx react-native run-android --deviceId=<device-id>
```

## Step 4: iOS Setup (macOS only)

### Install Xcode

1. Install Xcode from the Mac App Store
2. Open Xcode and accept the license agreement
3. Install Command Line Tools:
```bash
xcode-select --install
```

### Install CocoaPods

```bash
sudo gem install cocoapods
```

### Install iOS Dependencies

```bash
cd ios
pod install
cd ..
```

### Configure Code Signing

1. Open `ios/VendorApp.xcworkspace` in Xcode
2. Select the project in the navigator
3. Select the **VendorApp** target
4. Go to **Signing & Capabilities**
5. Select your development team
6. Xcode will automatically create a provisioning profile

### Run on iOS

```bash
# Start Metro bundler
npm start

# In another terminal, run on iOS
npm run ios

# Or run on specific simulator
npx react-native run-ios --simulator="iPhone 14"
```

## Step 5: Verify Installation

### Check React Native Environment

```bash
npx react-native doctor
```

This will check your environment and report any issues.

### Test the App

1. The app should launch on your emulator/simulator
2. You should see the "Vendor App" welcome screen
3. Check the Metro bundler logs for any errors

## Common Issues and Solutions

### Android Issues

**Issue: SDK location not found**
```bash
# Create local.properties file in android/
echo "sdk.dir=/Users/YOUR_USERNAME/Library/Android/sdk" > android/local.properties
```

**Issue: Gradle build fails**
```bash
cd android
./gradlew clean
cd ..
npm start -- --reset-cache
```

**Issue: Unable to load script**
```bash
# Clear Metro cache
npm start -- --reset-cache

# Clear Android build
cd android && ./gradlew clean && cd ..
```

### iOS Issues

**Issue: CocoaPods installation fails**
```bash
cd ios
pod deintegrate
pod install
cd ..
```

**Issue: Build fails in Xcode**
```bash
# Clean build folder
cd ios
xcodebuild clean
cd ..

# Reinstall pods
cd ios
rm -rf Pods Podfile.lock
pod install
cd ..
```

**Issue: Module not found**
```bash
# Clear watchman
watchman watch-del-all

# Clear Metro cache
npm start -- --reset-cache
```

### General Issues

**Issue: Metro bundler not starting**
```bash
# Kill any existing Metro processes
lsof -ti:8081 | xargs kill -9

# Start fresh
npm start -- --reset-cache
```

**Issue: Node modules issues**
```bash
# Clean install
rm -rf node_modules
npm install

# For iOS
cd ios && pod install && cd ..
```

## Development Workflow

### Running the App

1. Start Metro bundler:
```bash
npm start
```

2. Run on platform:
```bash
npm run android  # For Android
npm run ios      # For iOS
```

### Hot Reloading

- Press `R` twice in the app to reload
- Or shake the device and select "Reload"
- Enable Fast Refresh in Dev Menu for automatic reloading

### Debugging

**React Native Debugger:**
1. Install [React Native Debugger](https://github.com/jhen0409/react-native-debugger)
2. Open the app
3. Shake device → "Debug" → Opens in debugger

**Chrome DevTools:**
1. Shake device → "Debug"
2. Opens Chrome at `http://localhost:8081/debugger-ui`

**Flipper:**
1. Install [Flipper](https://fbflipper.com/)
2. Run the app
3. Flipper automatically connects

### Running Tests

```bash
# Run all tests
npm test

# Run in watch mode
npm run test:watch

# Generate coverage
npm run test:coverage
```

### Linting and Formatting

```bash
# Run linter
npm run lint

# Format code
npm run format
```

## Building for Production

### Android Release Build

1. Generate release keystore:
```bash
keytool -genkeypair -v -storetype PKCS12 -keystore release.keystore -alias release -keyalg RSA -keysize 2048 -validity 10000
```

2. Configure signing in `android/gradle.properties`:
```properties
RELEASE_STORE_FILE=release.keystore
RELEASE_KEY_ALIAS=release
RELEASE_STORE_PASSWORD=your_password
RELEASE_KEY_PASSWORD=your_password
```

3. Build release APK:
```bash
cd android
./gradlew assembleRelease
```

APK location: `android/app/build/outputs/apk/release/app-release.apk`

### iOS Release Build

1. Open `ios/VendorApp.xcworkspace` in Xcode
2. Select **Product** → **Archive**
3. Once archived, click **Distribute App**
4. Follow the wizard to export IPA

## Next Steps

1. Review the [README.md](./README.md) for project overview
2. Check [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) for code organization
3. Start implementing features from the tasks list
4. Write tests for new features
5. Follow the coding standards and best practices

## Getting Help

- Check React Native documentation: https://reactnative.dev/
- Review troubleshooting guide: https://reactnative.dev/docs/troubleshooting
- Check GitHub issues for common problems
- Contact the development team

## Resources

- [React Native Documentation](https://reactnative.dev/)
- [React Navigation](https://reactnavigation.org/)
- [Redux Toolkit](https://redux-toolkit.js.org/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [AWS Amplify](https://docs.amplify.aws/)

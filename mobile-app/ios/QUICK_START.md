# iOS Quick Start Guide

## Prerequisites

Before you begin, ensure you have:

- ✅ macOS (required for iOS development)
- ✅ Xcode 14.0 or later installed
- ✅ CocoaPods installed (`sudo gem install cocoapods`)
- ✅ Node.js 18+ and npm 9+
- ✅ React Native CLI (`npm install -g react-native-cli`)
- ✅ Apple Developer account (for device testing)

## Quick Setup (5 Minutes)

### 1. Install Dependencies

```bash
# From the mobile-app root directory
npm install

# Install iOS pods
cd ios
pod install
cd ..
```

### 2. Run on Simulator

```bash
# Start Metro bundler
npm start

# In another terminal, run on iOS simulator
npm run ios
```

That's it! The app should launch in the iOS Simulator.

## Run on Physical Device

### Option 1: Automatic Signing (Easiest)

1. Open the workspace in Xcode:
   ```bash
   open ios/VendorApp.xcworkspace
   ```

2. In Xcode:
   - Select the VendorApp target
   - Go to "Signing & Capabilities"
   - Enable "Automatically manage signing"
   - Select your Apple Developer team
   - Connect your iPhone via USB
   - Select your device from the device dropdown
   - Click the Run button (▶️)

### Option 2: Command Line

```bash
# Connect your iPhone via USB
# Trust the computer on your iPhone
npx react-native run-ios --device="Your iPhone Name"
```

## Build for Release

### Create Archive

1. Open workspace:
   ```bash
   open ios/VendorApp.xcworkspace
   ```

2. In Xcode:
   - Select "Any iOS Device" from device dropdown
   - Product → Archive
   - Wait for build to complete
   - Organizer window opens automatically

### Export IPA

In Xcode Organizer:
1. Select your archive
2. Click "Distribute App"
3. Choose distribution method:
   - **App Store Connect**: For App Store submission
   - **Ad Hoc**: For testing on registered devices
   - **Development**: For development testing
4. Follow the wizard to export

## Common Commands

```bash
# Install pods
cd ios && pod install && cd ..

# Run on default simulator
npm run ios

# Run on specific simulator
npx react-native run-ios --simulator="iPhone 14 Pro"

# Run on device
npx react-native run-ios --device

# Clean build
cd ios
xcodebuild clean
rm -rf ~/Library/Developer/Xcode/DerivedData/*
cd ..

# Reset Metro cache
npm start -- --reset-cache
```

## Troubleshooting

### "Command not found: pod"
```bash
sudo gem install cocoapods
```

### "Unable to find a destination matching the provided destination specifier"
```bash
# List available simulators
xcrun simctl list devices

# Run on specific simulator
npx react-native run-ios --simulator="iPhone 14"
```

### Build fails after pod install
```bash
# Clean and reinstall
cd ios
rm -rf Pods Podfile.lock
pod install --repo-update
cd ..
```

### Metro bundler issues
```bash
# Kill any running Metro processes
killall node

# Clear cache and restart
npm start -- --reset-cache
```

### Code signing errors
- Ensure you're logged into Xcode with your Apple ID
- Go to Xcode → Preferences → Accounts
- Add your Apple ID if not present
- Enable "Automatically manage signing" in project settings

## Simulator Shortcuts

- **⌘ + R**: Reload app
- **⌘ + D**: Open developer menu
- **⌘ + K**: Toggle keyboard
- **⌘ + Shift + H**: Home button
- **⌘ + Shift + H + H**: App switcher

## Next Steps

1. ✅ App running on simulator/device
2. 📱 Test all features (camera, microphone, location)
3. 🔧 Configure environment variables in `.env`
4. 🚀 Build for release when ready

## Need Help?

- Check `IOS_BUILD_SETUP.md` for detailed configuration
- Review React Native iOS documentation
- Check the troubleshooting section above

---

**Happy Coding! 🚀**

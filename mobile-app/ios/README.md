# iOS Build Configuration

This directory contains the iOS-specific configuration for the Vendor App mobile application.

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[QUICK_START.md](./QUICK_START.md)** | Quick setup guide - start here! |
| **[IOS_BUILD_SETUP.md](./IOS_BUILD_SETUP.md)** | Comprehensive build configuration guide |
| **[CONFIGURATION_SUMMARY.md](./CONFIGURATION_SUMMARY.md)** | Configuration status and checklist |

## 🚀 Quick Start

### 1. Verify Setup
```bash
./verify-setup.sh
```

### 2. Install Dependencies
```bash
pod install
```

### 3. Run on Simulator
```bash
cd ..
npm run ios
```

## 📋 Configuration Overview

### Platform
- **Minimum iOS Version**: 12.0
- **Target Devices**: iPhone 6s and newer
- **Hermes Engine**: Enabled

### Permissions Configured
- ✅ Camera (for freshness scanning)
- ✅ Microphone (for voice transactions)
- ✅ Location (for distance calculation)
- ✅ Photo Library (for marketplace listings)
- ✅ Notifications (for alerts)

### Native Dependencies
- React Native Camera
- React Native Voice
- React Native Geolocation
- React Native Vector Icons
- React Native Permissions

## 🔧 Build Commands

```bash
# Install pods
pod install

# Run on simulator
npm run ios

# Run on specific simulator
npx react-native run-ios --simulator="iPhone 14"

# Run on device
npx react-native run-ios --device

# Clean build
xcodebuild clean
rm -rf ~/Library/Developer/Xcode/DerivedData/*

# Verify setup
./verify-setup.sh
```

## 📱 Build Schemes

### Debug
- For development and testing
- Automatic code signing
- Debug symbols included

### Release
- For App Store distribution
- Manual code signing required
- Optimizations enabled
- Debug symbols stripped

## 🔐 Code Signing

### Development (Debug)
1. Open `VendorApp.xcworkspace` in Xcode
2. Select VendorApp target
3. Go to "Signing & Capabilities"
4. Enable "Automatically manage signing"
5. Select your team

### Production (Release)
1. Create Distribution certificate in Apple Developer Portal
2. Create App Store provisioning profile
3. Configure in Xcode under "Signing & Capabilities"
4. Disable "Automatically manage signing"
5. Select Distribution certificate and profile

## 📦 Project Structure

```
ios/
├── Podfile                      # CocoaPods dependencies
├── Podfile.lock                 # Locked dependency versions
├── Pods/                        # Installed pods (generated)
├── VendorApp.xcworkspace        # Xcode workspace (generated)
├── VendorApp/
│   ├── Info.plist              # App configuration and permissions
│   ├── Images.xcassets/        # App icons and images
│   └── LaunchScreen.storyboard # Splash screen
├── IOS_BUILD_SETUP.md          # Detailed setup guide
├── QUICK_START.md              # Quick start guide
├── CONFIGURATION_SUMMARY.md    # Configuration checklist
├── verify-setup.sh             # Setup verification script
└── README.md                   # This file
```

## ⚠️ Important Notes

- **Always open `VendorApp.xcworkspace`**, not the `.xcodeproj` file
- Run `pod install` after adding new dependencies
- Clean build if you encounter issues
- Test on physical devices for camera, microphone, location features
- macOS and Xcode are required for iOS development

## 🐛 Troubleshooting

### Common Issues

**Pod install fails:**
```bash
pod cache clean --all
rm -rf Pods Podfile.lock
pod install --repo-update
```

**Build fails:**
```bash
xcodebuild clean
rm -rf ~/Library/Developer/Xcode/DerivedData/*
```

**Metro bundler issues:**
```bash
npm start -- --reset-cache
```

**Code signing errors:**
- Verify Apple Developer account is active
- Check certificate expiration
- Try "Automatically manage signing"

See [IOS_BUILD_SETUP.md](./IOS_BUILD_SETUP.md) for more troubleshooting tips.

## 📊 Performance Targets

| Metric | Target | Status |
|--------|--------|--------|
| App Size | < 50MB | ⏳ Pending |
| Launch Time | < 3 seconds | ⏳ Pending |
| Memory Usage | < 200MB | ⏳ Pending |

## 🎯 Requirements Met

- ✅ iOS 12.0+ support
- ✅ iPhone 6s+ compatibility
- ✅ Camera permission configured
- ✅ Microphone permission configured
- ✅ Location permission configured
- ✅ CocoaPods dependencies configured
- ✅ Build schemes configured
- ✅ Hermes engine enabled

## 📞 Need Help?

1. Check the documentation files in this directory
2. Run `./verify-setup.sh` to diagnose issues
3. Review [React Native iOS Setup](https://reactnative.dev/docs/environment-setup)
4. Consult the development team

---

**Ready to build?** Start with [QUICK_START.md](./QUICK_START.md)!

# iOS Build Configuration Guide

## Overview

This document describes the iOS build configuration for the Vendor App mobile application. The app targets iOS 12.0+ to support older iPhone models (iPhone 6s and above) as specified in the requirements.

## Build Configuration Summary

### Minimum Requirements
- **iOS Version**: 12.0+
- **Xcode**: 14.0+
- **CocoaPods**: 1.11.0+
- **macOS**: Required for iOS development
- **Apple Developer Account**: Required for device testing and App Store distribution

### Target Devices
- iPhone 6s and newer
- iPad (5th generation and newer)
- Optimized for devices with 2GB RAM

## Podfile Configuration

The `Podfile` is configured with:

### Platform
```ruby
platform :ios, '12.0'
```

### Core Dependencies
- **React Native**: Core framework with Hermes engine enabled
- **React Native Camera**: For produce freshness scanning
- **React Native Voice**: For Hindi voice transaction recording
- **React Native Geolocation**: For distance calculation to mandis
- **React Native Vector Icons**: For UI icons

### Permissions
The following permissions are configured:
- **Camera**: For freshness scanning
- **Microphone**: For voice transaction recording
- **Location (When In Use)**: For distance calculation
- **Notifications**: For price alerts and buyer interest
- **Photo Library**: For marketplace listing images

## Info.plist Permissions

All required permission descriptions are configured in `VendorApp/Info.plist`:

```xml
<key>NSCameraUsageDescription</key>
<string>We need camera access to scan produce for freshness classification</string>

<key>NSMicrophoneUsageDescription</key>
<string>We need microphone access to record voice transactions in Hindi</string>

<key>NSLocationWhenInUseUsageDescription</key>
<string>We need your location to show nearby mandi prices and calculate distances</string>

<key>NSPhotoLibraryUsageDescription</key>
<string>We need photo library access to select images for marketplace listings</string>
```

## Build Schemes

### Debug Scheme
- **Purpose**: Development and testing
- **Configuration**: Debug
- **Code Signing**: Automatic (Development)
- **Optimizations**: Disabled
- **Hermes**: Enabled for better performance

### Release Scheme
- **Purpose**: Production builds for App Store
- **Configuration**: Release
- **Code Signing**: Manual (Distribution)
- **Optimizations**: Enabled
- **Bitcode**: Disabled (React Native requirement)
- **Strip Debug Symbols**: Enabled

## Code Signing Setup

### Development (Debug Builds)

1. **Automatic Signing** (Recommended for development):
   - Open `VendorApp.xcworkspace` in Xcode
   - Select the VendorApp target
   - Go to "Signing & Capabilities"
   - Enable "Automatically manage signing"
   - Select your development team

2. **Manual Signing**:
   - Create a Development certificate in Apple Developer Portal
   - Create a Development provisioning profile
   - Download and install both
   - Configure in Xcode under "Signing & Capabilities"

### Production (Release Builds)

1. **Create Distribution Certificate**:
   ```bash
   # Generate certificate signing request (CSR)
   # Go to Keychain Access > Certificate Assistant > Request a Certificate
   # Save the CSR file
   ```

2. **Apple Developer Portal**:
   - Go to Certificates, Identifiers & Profiles
   - Create an App Store Distribution certificate using the CSR
   - Download and install the certificate

3. **Create App ID**:
   - Bundle Identifier: `com.vendorapp.mobile` (or your chosen ID)
   - Enable capabilities: Push Notifications, Background Modes

4. **Create Provisioning Profile**:
   - Type: App Store Distribution
   - Select your App ID
   - Select your Distribution certificate
   - Download and install the profile

5. **Configure in Xcode**:
   - Open `VendorApp.xcworkspace`
   - Select VendorApp target
   - Go to "Signing & Capabilities"
   - Disable "Automatically manage signing"
   - Select your Distribution certificate and provisioning profile

## Build Commands

### Install Dependencies
```bash
cd ios
pod install
cd ..
```

### Run on Simulator (Debug)
```bash
npm run ios
# Or specify simulator
npx react-native run-ios --simulator="iPhone 14"
```

### Run on Device (Debug)
```bash
npx react-native run-ios --device="Your iPhone Name"
```

### Build for Release (Archive)
```bash
# Open Xcode
open ios/VendorApp.xcworkspace

# In Xcode:
# 1. Select "Any iOS Device" or your connected device
# 2. Product > Archive
# 3. Wait for archive to complete
# 4. Organizer window will open automatically
```

### Export IPA for App Store
```bash
# In Xcode Organizer:
# 1. Select your archive
# 2. Click "Distribute App"
# 3. Select "App Store Connect"
# 4. Follow the wizard to upload
```

### Export IPA for Ad Hoc Distribution
```bash
# In Xcode Organizer:
# 1. Select your archive
# 2. Click "Distribute App"
# 3. Select "Ad Hoc"
# 4. Select provisioning profile
# 5. Export IPA file
```

## Build Settings

### Key Build Settings in Xcode

| Setting | Debug | Release |
|---------|-------|---------|
| Deployment Target | iOS 12.0 | iOS 12.0 |
| Enable Bitcode | No | No |
| Strip Debug Symbols | No | Yes |
| Optimization Level | None [-O0] | Fastest, Smallest [-Os] |
| Dead Code Stripping | No | Yes |
| Enable Testability | Yes | No |

### Recommended Settings for Performance

1. **Enable Hermes Engine** (Already configured in Podfile):
   - Faster app startup
   - Reduced memory usage
   - Smaller bundle size

2. **Optimize Images**:
   - Use asset catalogs
   - Enable compression
   - Use appropriate image scales (@1x, @2x, @3x)

3. **Enable Dead Code Stripping**:
   - Reduces final app size
   - Removes unused code

## Troubleshooting

### Common Issues

#### 1. Pod Install Fails
```bash
# Clear CocoaPods cache
pod cache clean --all
rm -rf ~/Library/Caches/CocoaPods
rm -rf Pods
rm Podfile.lock

# Reinstall
pod install --repo-update
```

#### 2. Build Fails with "Command PhaseScriptExecution failed"
```bash
# Clean build folder
cd ios
xcodebuild clean
rm -rf ~/Library/Developer/Xcode/DerivedData/*

# Rebuild
cd ..
npm run ios
```

#### 3. Code Signing Issues
- Verify your Apple Developer account is active
- Check certificate expiration dates
- Ensure provisioning profile matches bundle identifier
- Try "Automatically manage signing" for development

#### 4. "Unable to boot simulator" Error
```bash
# Reset simulator
xcrun simctl erase all
# Or reset specific simulator in Xcode
```

#### 5. Metro Bundler Issues
```bash
# Clear Metro cache
npm start -- --reset-cache
```

## Performance Optimization

### App Size Optimization
- Current target: < 50MB
- Enable bitcode stripping
- Use asset compression
- Remove unused resources

### Launch Time Optimization
- Target: < 3 seconds
- Hermes engine enabled
- Lazy load non-critical modules
- Optimize splash screen

### Memory Optimization
- Target: < 200MB on 2GB RAM devices
- Use image compression
- Implement proper memory management
- Profile with Instruments

## Testing on Physical Devices

### Development Testing
1. Connect iPhone via USB
2. Trust the computer on iPhone
3. Run: `npx react-native run-ios --device`
4. App will install and launch

### TestFlight Distribution
1. Archive the app in Xcode
2. Upload to App Store Connect
3. Add internal/external testers
4. Testers receive TestFlight invitation
5. Install via TestFlight app

## App Store Submission Checklist

- [ ] App built with Release configuration
- [ ] Code signing configured with Distribution certificate
- [ ] App Store provisioning profile selected
- [ ] Version and build number incremented
- [ ] All required permissions have usage descriptions
- [ ] App tested on physical devices (iOS 12, 13, 14, 15, 16)
- [ ] Screenshots prepared (all required sizes)
- [ ] App description written (English + Hindi)
- [ ] Privacy policy URL provided
- [ ] App icons prepared (all required sizes)
- [ ] Archive uploaded to App Store Connect
- [ ] App metadata completed in App Store Connect
- [ ] Submitted for review

## Build Schemes Configuration

### Creating Custom Schemes

1. **Open Scheme Editor**:
   - Product > Scheme > Edit Scheme

2. **Debug Scheme**:
   - Build Configuration: Debug
   - Executable: VendorApp.app
   - Debug executable: Enabled
   - Launch automatically: Enabled

3. **Release Scheme**:
   - Build Configuration: Release
   - Executable: VendorApp.app
   - Debug executable: Disabled
   - Launch automatically: Enabled

### Environment Variables in Schemes

Add environment variables for different configurations:
- `API_BASE_URL`: Backend API endpoint
- `AWS_REGION`: AWS region
- `S3_BUCKET_NAME`: S3 bucket for uploads
- `ENVIRONMENT`: dev/staging/production

## Continuous Integration

### Fastlane Setup (Optional)
```bash
# Install Fastlane
sudo gem install fastlane

# Initialize
cd ios
fastlane init

# Configure lanes for build and deploy
```

### Example Fastlane Configuration
```ruby
lane :beta do
  build_app(scheme: "VendorApp")
  upload_to_testflight
end

lane :release do
  build_app(scheme: "VendorApp")
  upload_to_app_store
end
```

## Security Considerations

### Code Signing Security
- Keep certificates and private keys secure
- Use separate certificates for development and distribution
- Rotate certificates before expiration
- Use Keychain for secure storage

### App Transport Security
- HTTPS required for all network requests
- Exceptions configured for localhost (development only)
- Remove exceptions for production builds

### Data Security
- Use Keychain for sensitive data storage
- Enable data protection
- Implement proper authentication
- Secure API keys and tokens

## Resources

### Official Documentation
- [React Native iOS Setup](https://reactnative.dev/docs/environment-setup)
- [Apple Developer Documentation](https://developer.apple.com/documentation/)
- [CocoaPods Guides](https://guides.cocoapods.org/)
- [Xcode Help](https://help.apple.com/xcode/)

### Useful Tools
- [Xcode](https://developer.apple.com/xcode/)
- [CocoaPods](https://cocoapods.org/)
- [Fastlane](https://fastlane.tools/)
- [TestFlight](https://developer.apple.com/testflight/)

## Support

For issues specific to this project:
1. Check this documentation
2. Review the troubleshooting section
3. Check React Native iOS documentation
4. Consult the development team

---

**Last Updated**: 2024
**iOS Version**: 12.0+
**React Native Version**: 0.73.0

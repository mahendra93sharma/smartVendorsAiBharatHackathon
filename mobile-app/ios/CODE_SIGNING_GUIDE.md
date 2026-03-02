# iOS Code Signing Guide

## Overview

Code signing is required to run iOS apps on physical devices and distribute them via the App Store. This guide covers both development and production code signing setup.

## Prerequisites

- Apple Developer account (free for development, $99/year for distribution)
- Xcode installed
- VendorApp project opened in Xcode

## Development Code Signing (Debug Builds)

### Option 1: Automatic Signing (Recommended)

This is the easiest method for development:

1. **Open the workspace in Xcode:**
   ```bash
   open VendorApp.xcworkspace
   ```

2. **Select the VendorApp target:**
   - Click on the VendorApp project in the navigator
   - Select the VendorApp target under TARGETS

3. **Configure automatic signing:**
   - Go to the "Signing & Capabilities" tab
   - Check "Automatically manage signing"
   - Select your Team from the dropdown
   - Xcode will automatically create certificates and profiles

4. **Verify configuration:**
   - Provisioning Profile should show "Xcode Managed Profile"
   - Signing Certificate should show "Apple Development"
   - Status should show "Ready to run"

### Option 2: Manual Signing

For more control over certificates and profiles:

1. **Create a Development Certificate:**
   - Open Keychain Access
   - Certificate Assistant → Request a Certificate from a Certificate Authority
   - Save the CSR file
   - Go to [Apple Developer Portal](https://developer.apple.com/account/)
   - Certificates, Identifiers & Profiles → Certificates
   - Click "+" to create new certificate
   - Select "iOS App Development"
   - Upload CSR and download certificate
   - Double-click to install in Keychain

2. **Register your device:**
   - Get device UDID from Xcode (Window → Devices and Simulators)
   - Go to Apple Developer Portal → Devices
   - Click "+" and register your device

3. **Create Development Provisioning Profile:**
   - Go to Profiles in Developer Portal
   - Click "+" to create new profile
   - Select "iOS App Development"
   - Select your App ID (or create one)
   - Select your Development certificate
   - Select your registered devices
   - Download and double-click to install

4. **Configure in Xcode:**
   - Uncheck "Automatically manage signing"
   - Select your Development certificate
   - Select your Development provisioning profile

## Production Code Signing (Release Builds)

### Step 1: Create Distribution Certificate

1. **Generate Certificate Signing Request (CSR):**
   ```bash
   # Open Keychain Access
   # Certificate Assistant → Request a Certificate from a Certificate Authority
   # Enter your email and name
   # Select "Saved to disk"
   # Save the CSR file
   ```

2. **Create Distribution Certificate:**
   - Go to [Apple Developer Portal](https://developer.apple.com/account/)
   - Certificates, Identifiers & Profiles → Certificates
   - Click "+" to create new certificate
   - Select "Apple Distribution" (for App Store and Ad Hoc)
   - Upload your CSR file
   - Download the certificate
   - Double-click to install in Keychain

3. **Verify installation:**
   ```bash
   # Open Keychain Access
   # Look for "Apple Distribution: Your Name (Team ID)"
   # Expand to see the private key
   ```

### Step 2: Create App ID

1. **Register App ID:**
   - Go to Identifiers in Developer Portal
   - Click "+" to create new identifier
   - Select "App IDs" → Continue
   - Select "App" → Continue

2. **Configure App ID:**
   - Description: "Vendor App"
   - Bundle ID: Explicit (e.g., `com.vendorapp.mobile`)
   - Capabilities: Enable required capabilities
     - Push Notifications
     - Background Modes (if needed)
   - Click Continue → Register

### Step 3: Create Provisioning Profile

#### For App Store Distribution:

1. **Create App Store Profile:**
   - Go to Profiles in Developer Portal
   - Click "+" to create new profile
   - Select "App Store" under Distribution
   - Select your App ID
   - Select your Distribution certificate
   - Name: "VendorApp App Store"
   - Download the profile

2. **Install the profile:**
   ```bash
   # Double-click the downloaded .mobileprovision file
   # Or drag it to Xcode
   ```

#### For Ad Hoc Distribution (Testing):

1. **Create Ad Hoc Profile:**
   - Select "Ad Hoc" under Distribution
   - Select your App ID
   - Select your Distribution certificate
   - Select devices for testing
   - Name: "VendorApp Ad Hoc"
   - Download and install

### Step 4: Configure Xcode for Release

1. **Open workspace:**
   ```bash
   open VendorApp.xcworkspace
   ```

2. **Select VendorApp target:**
   - Click on project in navigator
   - Select VendorApp target

3. **Configure Release signing:**
   - Go to "Signing & Capabilities" tab
   - Uncheck "Automatically manage signing"
   - Under "Release" configuration:
     - Provisioning Profile: Select your Distribution profile
     - Signing Certificate: Select your Distribution certificate

4. **Verify configuration:**
   - Status should show "Ready to archive"
   - No errors or warnings

## Build Configurations

### Debug Configuration

| Setting | Value |
|---------|-------|
| Code Signing Identity | Apple Development |
| Provisioning Profile | Automatic or Development |
| Code Signing Style | Automatic or Manual |

### Release Configuration

| Setting | Value |
|---------|-------|
| Code Signing Identity | Apple Distribution |
| Provisioning Profile | App Store or Ad Hoc |
| Code Signing Style | Manual |

## Creating Builds

### Debug Build (Development)

```bash
# Run on simulator
npm run ios

# Run on connected device
npx react-native run-ios --device="Your iPhone"
```

### Release Build (Archive)

1. **Select build destination:**
   - In Xcode, select "Any iOS Device" from device dropdown

2. **Create archive:**
   - Product → Archive
   - Wait for build to complete
   - Organizer window opens automatically

3. **Verify archive:**
   - Check that signing is correct
   - No errors or warnings

### Export IPA

#### For App Store:

1. In Organizer, select your archive
2. Click "Distribute App"
3. Select "App Store Connect"
4. Click "Upload"
5. Follow wizard to upload to App Store Connect

#### For Ad Hoc Testing:

1. In Organizer, select your archive
2. Click "Distribute App"
3. Select "Ad Hoc"
4. Select provisioning profile
5. Export IPA file
6. Distribute IPA to testers

## Troubleshooting

### "No signing certificate found"

**Solution:**
- Verify certificate is installed in Keychain
- Check certificate hasn't expired
- Ensure private key is present
- Try creating a new certificate

### "No provisioning profiles found"

**Solution:**
- Download profile from Developer Portal
- Double-click to install
- Refresh profiles in Xcode (Preferences → Accounts → Download Manual Profiles)

### "Code signing is required for product type 'Application'"

**Solution:**
- Ensure signing is configured for both Debug and Release
- Check that bundle identifier matches App ID
- Verify team is selected

### "The executable was signed with invalid entitlements"

**Solution:**
- Verify App ID capabilities match entitlements
- Regenerate provisioning profile
- Clean build folder and rebuild

### "Unable to install app on device"

**Solution:**
- Check device is registered in Developer Portal
- Verify device UDID is correct
- Ensure provisioning profile includes the device
- Trust the developer certificate on device (Settings → General → Device Management)

## Certificate Management

### Certificate Expiration

- **Development certificates**: Valid for 1 year
- **Distribution certificates**: Valid for 1 year
- Set calendar reminders to renew before expiration

### Renewing Certificates

1. Revoke old certificate in Developer Portal
2. Create new certificate following steps above
3. Update provisioning profiles with new certificate
4. Download and install updated profiles

### Backup Certificates

**Important:** Back up your certificates and private keys!

```bash
# Export from Keychain Access:
# 1. Select certificate
# 2. File → Export Items
# 3. Save as .p12 file
# 4. Set a strong password
# 5. Store securely (password manager, encrypted storage)
```

### Sharing Certificates (Team)

For team development:

1. Export certificate as .p12 file
2. Share securely with team members
3. Team members import into their Keychain
4. Share provisioning profiles

## Best Practices

### Security

- ✅ Keep private keys secure
- ✅ Use strong passwords for .p12 exports
- ✅ Don't commit certificates to version control
- ✅ Rotate certificates regularly
- ✅ Revoke compromised certificates immediately

### Organization

- ✅ Use descriptive names for profiles
- ✅ Document certificate ownership
- ✅ Maintain certificate inventory
- ✅ Set expiration reminders
- ✅ Keep backup of certificates

### Development

- ✅ Use automatic signing for development
- ✅ Use manual signing for production
- ✅ Test on physical devices regularly
- ✅ Verify signing before archiving
- ✅ Keep Xcode and tools updated

## Continuous Integration

### Fastlane Setup

For automated builds and signing:

```ruby
# Fastfile
lane :beta do
  match(type: "adhoc")
  build_app(scheme: "VendorApp")
  upload_to_testflight
end

lane :release do
  match(type: "appstore")
  build_app(scheme: "VendorApp")
  upload_to_app_store
end
```

### Match (Certificate Management)

```bash
# Install Fastlane
sudo gem install fastlane

# Initialize Match
fastlane match init

# Generate certificates
fastlane match development
fastlane match appstore
```

## Resources

### Official Documentation
- [Apple Code Signing Guide](https://developer.apple.com/support/code-signing/)
- [App Distribution Guide](https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases)
- [Xcode Help](https://help.apple.com/xcode/)

### Tools
- [Apple Developer Portal](https://developer.apple.com/account/)
- [App Store Connect](https://appstoreconnect.apple.com/)
- [Fastlane](https://fastlane.tools/)

### Support
- [Apple Developer Forums](https://developer.apple.com/forums/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/ios-code-signing)

---

**Need Help?** Check the troubleshooting section or consult the development team.

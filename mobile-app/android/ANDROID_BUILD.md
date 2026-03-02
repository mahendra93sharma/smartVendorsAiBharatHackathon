# Android Build Configuration Guide

## Overview

This document describes the Android build configuration for the Vendor App, including signing keys, ProGuard setup, and release build process.

## Build Configuration

### SDK Versions
- **minSdkVersion**: 21 (Android 5.0 Lollipop)
- **targetSdkVersion**: 33 (Android 13)
- **compileSdkVersion**: 33

### Multi-Dex Support
Multi-dex is enabled to support apps with more than 65,536 methods. This is configured in `app/build.gradle`:
```gradle
multiDexEnabled true
```

### Hermes Engine
Hermes JavaScript engine is enabled for improved performance:
```gradle
enableHermes = true
```

## Permissions

The following permissions are configured in `AndroidManifest.xml`:

### Required Permissions
- `INTERNET` - Network access for API calls
- `CAMERA` - Camera access for produce scanning
- `RECORD_AUDIO` - Microphone access for voice transactions
- `ACCESS_FINE_LOCATION` - GPS location for distance calculations
- `ACCESS_COARSE_LOCATION` - Network-based location fallback
- `ACCESS_NETWORK_STATE` - Detect online/offline status
- `VIBRATE` - Haptic feedback
- `POST_NOTIFICATIONS` - Push notifications (Android 13+)

### Storage Permissions
- `READ_EXTERNAL_STORAGE` - Read images from gallery
- `WRITE_EXTERNAL_STORAGE` - Save temporary files

### Hardware Features
All hardware features are marked as `required="false"` to allow installation on devices without these features:
- Camera
- Camera autofocus
- Microphone
- GPS

## ProGuard Configuration

ProGuard is enabled for release builds to:
- Minify code (reduce APK size)
- Obfuscate code (security)
- Remove unused code

### ProGuard Rules

The `proguard-rules.pro` file includes rules for:

1. **React Native**: Keep React Native core classes
2. **Hermes**: Keep Hermes engine classes
3. **AWS SDK**: Keep AWS service classes
4. **OkHttp**: Keep networking classes
5. **Gson**: Keep JSON serialization classes
6. **Native Methods**: Keep all native method declarations
7. **Debug Info**: Keep line numbers for crash reports

### Resource Shrinking

Resource shrinking is enabled in release builds to remove unused resources:
```gradle
shrinkResources true
```

## Signing Configuration

### Debug Signing

Debug builds use the default Android debug keystore:
- **Keystore**: `debug.keystore`
- **Password**: `android`
- **Alias**: `androiddebugkey`
- **Key Password**: `android`

### Release Signing

Release builds use environment variables for security. The keystore file should **never** be committed to version control.

#### Environment Variables

Set these environment variables before building:

```bash
export KEYSTORE_FILE=/path/to/release.keystore
export KEYSTORE_PASSWORD=your_keystore_password
export KEY_ALIAS=your_key_alias
export KEY_PASSWORD=your_key_password
```

#### Generating a Release Keystore

To generate a new release keystore:

```bash
keytool -genkeypair -v \
  -storetype PKCS12 \
  -keystore release.keystore \
  -alias vendor-app-key \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000
```

You will be prompted for:
- Keystore password (choose a strong password)
- Key password (can be same as keystore password)
- Your name, organization, city, state, country

**Important**: Store the keystore file and passwords securely. If you lose them, you cannot update your app on Google Play Store.

#### Keystore Storage Recommendations

1. **Never commit keystore to Git**: Add `*.keystore` to `.gitignore`
2. **Backup securely**: Store in a password manager or secure cloud storage
3. **Document passwords**: Keep passwords in a secure location
4. **Team access**: Use a shared secure storage for team access

## Building the App

### Debug Build

Build and install debug APK:
```bash
cd android
./gradlew installDebug
```

Or use React Native CLI:
```bash
npx react-native run-android
```

### Release Build

#### Build Release APK

```bash
cd android
./gradlew assembleRelease
```

Output: `android/app/build/outputs/apk/release/app-release.apk`

#### Build Release AAB (for Google Play)

```bash
cd android
./gradlew bundleRelease
```

Output: `android/app/build/outputs/bundle/release/app-release.aab`

### Build with Environment Variables

```bash
export KEYSTORE_FILE=~/secure/release.keystore
export KEYSTORE_PASSWORD=your_password
export KEY_ALIAS=vendor-app-key
export KEY_PASSWORD=your_key_password

cd android
./gradlew assembleRelease
```

## Testing Release Builds

### Install Release APK

```bash
adb install android/app/build/outputs/apk/release/app-release.apk
```

### Verify ProGuard

Check that ProGuard is working:
1. Compare APK sizes (release should be smaller)
2. Decompile APK and verify obfuscation
3. Test all features work correctly

### Test on Multiple Devices

Test release builds on:
- Android 5.0 (API 21) - minimum supported version
- Android 8.0 (API 26) - common version
- Android 13 (API 33) - target version
- Low-end device (2GB RAM)
- High-end device

## APK Size Optimization

Current optimizations:
- Hermes engine (smaller bundle)
- ProGuard minification
- Resource shrinking
- Native library stripping

Target APK size: < 50MB

## Troubleshooting

### Build Fails with "Keystore not found"

Ensure `KEYSTORE_FILE` environment variable points to the correct file:
```bash
echo $KEYSTORE_FILE
ls -la $KEYSTORE_FILE
```

### ProGuard Errors

If ProGuard causes runtime errors:
1. Check ProGuard rules in `proguard-rules.pro`
2. Add keep rules for affected classes
3. Test thoroughly after adding rules

### Multi-Dex Issues

If you encounter "method limit exceeded":
1. Verify `multiDexEnabled true` is set
2. Clean and rebuild: `./gradlew clean assembleRelease`

### Hermes Issues

If Hermes causes problems:
1. Disable Hermes: `enableHermes = false`
2. Clean build: `./gradlew clean`
3. Rebuild app

## Google Play Store Submission

### Prepare for Submission

1. Build release AAB (not APK)
2. Test AAB thoroughly
3. Prepare store listing:
   - App name and description
   - Screenshots (phone and tablet)
   - Feature graphic (1024x500)
   - App icon (512x512)
   - Privacy policy URL
   - Content rating

### Upload to Play Console

1. Go to [Google Play Console](https://play.google.com/console)
2. Create new app or select existing
3. Navigate to "Release" → "Production"
4. Upload AAB file
5. Fill in release notes
6. Submit for review

### Version Management

Update version in `app/build.gradle`:
```gradle
versionCode 2  // Increment for each release
versionName "1.0.1"  // Semantic versioning
```

## CI/CD Integration

### GitHub Actions Example

```yaml
- name: Build Release APK
  env:
    KEYSTORE_FILE: ${{ secrets.KEYSTORE_FILE }}
    KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
    KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
    KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
  run: |
    cd android
    ./gradlew assembleRelease
```

Store keystore as base64 in GitHub Secrets:
```bash
base64 release.keystore > keystore.base64
```

## Security Best Practices

1. **Never commit keystores**: Add to `.gitignore`
2. **Use environment variables**: Don't hardcode passwords
3. **Rotate keys carefully**: Google Play allows key rotation
4. **Enable Play App Signing**: Let Google manage signing keys
5. **Monitor for tampering**: Use Play Integrity API

## Performance Monitoring

After release:
- Monitor crash reports in Play Console
- Check ANR (Application Not Responding) rates
- Monitor app size and download metrics
- Track performance metrics

## References

- [Android Developer Guide](https://developer.android.com/studio/build)
- [ProGuard Manual](https://www.guardsquare.com/manual/home)
- [React Native Android Setup](https://reactnative.dev/docs/signed-apk-android)
- [Google Play Console](https://play.google.com/console)

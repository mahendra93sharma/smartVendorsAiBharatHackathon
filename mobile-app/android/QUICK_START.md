# Android Build Quick Start

## Prerequisites

- Android Studio installed
- Android SDK (API 21-33)
- Java JDK 11
- Node.js and npm

## Development Build

```bash
# From project root
npx react-native run-android

# Or from android directory
cd android
./gradlew installDebug
```

## Release Build Setup (First Time Only)

### 1. Generate Release Keystore

```bash
cd android
bash generate-keystore.sh
```

Follow the prompts to create your keystore. **Save the passwords securely!**

### 2. Set Environment Variables

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
export KEYSTORE_FILE=/path/to/your/release.keystore
export KEYSTORE_PASSWORD=your_keystore_password
export KEY_ALIAS=vendor-app-key
export KEY_PASSWORD=your_key_password
```

Then reload: `source ~/.bashrc` or `source ~/.zshrc`

## Build Release APK

```bash
cd android
./gradlew assembleRelease
```

Output: `android/app/build/outputs/apk/release/app-release.apk`

## Build Release AAB (for Play Store)

```bash
cd android
./gradlew bundleRelease
```

Output: `android/app/build/outputs/bundle/release/app-release.aab`

## Install Release APK on Device

```bash
adb install android/app/build/outputs/apk/release/app-release.apk
```

## Clean Build

If you encounter issues:

```bash
cd android
./gradlew clean
./gradlew assembleRelease
```

## Verify Configuration

Check that all settings are correct:

```bash
# Check SDK versions
grep -E "(minSdkVersion|targetSdkVersion|compileSdkVersion)" android/build.gradle

# Check multi-dex
grep "multiDexEnabled" android/app/build.gradle

# Check ProGuard
grep "minifyEnabled" android/app/build.gradle

# Check permissions
grep "uses-permission" android/app/src/main/AndroidManifest.xml
```

## Common Issues

### Issue: "Keystore not found"
**Solution**: Ensure `KEYSTORE_FILE` environment variable is set and points to the correct file.

### Issue: "Build failed with ProGuard"
**Solution**: Check `proguard-rules.pro` and add keep rules for affected classes.

### Issue: "Multi-dex error"
**Solution**: Verify `multiDexEnabled true` is set in `app/build.gradle`.

## Configuration Summary

✅ **minSdkVersion**: 21 (Android 5.0+)
✅ **targetSdkVersion**: 33 (Android 13)
✅ **Multi-dex**: Enabled
✅ **ProGuard**: Enabled for release builds
✅ **Hermes**: Enabled
✅ **Permissions**: CAMERA, RECORD_AUDIO, INTERNET, ACCESS_FINE_LOCATION
✅ **Signing**: Configured with environment variables

## Next Steps

1. Test debug build on device
2. Generate release keystore
3. Build release APK
4. Test release APK thoroughly
5. Build AAB for Play Store submission

For detailed information, see [ANDROID_BUILD.md](./ANDROID_BUILD.md)

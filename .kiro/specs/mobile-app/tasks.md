# Implementation Plan: React Native Mobile App (Android & iOS)

## Overview

This implementation plan focuses on creating native mobile applications (Android and iOS) using React Native CLI that replicate all features from the web frontend. The mobile apps will connect to the existing AWS backend infrastructure (Lambda functions, DynamoDB, S3) via API Gateway. The approach prioritizes native mobile UX patterns, offline-first architecture, device-specific features (camera, microphone, geolocation), and performance optimization for low-end devices (2GB RAM). Tasks are organized to build incrementally, starting with project setup, then core features, AWS integration, and finally platform-specific builds.

## Architecture Stack

- **React Native CLI**: Native mobile framework (not Expo)
- **TypeScript**: Type-safe development
- **React Navigation**: Native navigation
- **AWS Amplify**: AWS service integration
- **AsyncStorage**: Local data persistence
- **React Native Voice**: Voice recording
- **React Native Camera**: Image capture
- **Axios**: HTTP client for API calls
- **Redux Toolkit**: State management

## Target Platforms

- **Android**: API Level 21+ (Android 5.0+)
- **iOS**: iOS 12.0+
- **Devices**: 2GB RAM minimum, optimized for budget smartphones

## Tasks

- [x] 1. Set up React Native CLI project structure
  - Initialize React Native project with TypeScript template
  - Configure project for both Android and iOS
  - Set up folder structure: src/screens, src/components, src/services, src/store, src/utils, src/types
  - Configure TypeScript with strict mode
  - Set up ESLint and Prettier for React Native
  - Configure Metro bundler for optimization
  - Set up environment variables with react-native-config
  - Create .env.example with API_BASE_URL, AWS_REGION, S3_BUCKET_NAME
  - _Requirements: Project foundation, code quality_

- [ ] 2. Configure native dependencies and build tools
  - [x] 2.1 Set up Android build configuration
    - Configure android/build.gradle with minSdkVersion 21, targetSdkVersion 33
    - Set up ProGuard for release builds
    - Configure signing keys for release APK
    - Add permissions in AndroidManifest.xml: CAMERA, RECORD_AUDIO, INTERNET, ACCESS_FINE_LOCATION
    - Configure Gradle for multi-dex support
    - _Requirements: Android platform support_
  
  - [x] 2.2 Set up iOS build configuration
    - Configure ios/Podfile with minimum iOS version 12.0
    - Set up CocoaPods dependencies
    - Configure Info.plist permissions: Camera, Microphone, Location
    - Set up code signing and provisioning profiles
    - Configure build schemes for Debug and Release
    - _Requirements: iOS platform support_
  
  - [ ] 2.3 Install and link native modules
    - Install React Navigation (native-stack, bottom-tabs)
    - Install React Native Voice for audio recording
    - Install React Native Camera for image capture
    - Install React Native Geolocation for location services
    - Install AsyncStorage for local persistence
    - Install React Native Vector Icons
    - Install React Native Gesture Handler
    - Link all native dependencies using pod install (iOS) and Gradle sync (Android)
    - _Requirements: Native functionality_

- [ ] 3. Set up AWS integration and API layer
  - [ ] 3.1 Configure AWS Amplify for React Native
    - Install AWS Amplify and AWS Amplify React Native
    - Configure Amplify with AWS region and API Gateway endpoint
    - Set up authentication configuration (if needed)
    - Configure S3 bucket access for image uploads
    - Test Amplify connection to backend
    - _Requirements: AWS backend integration_
  
  - [ ] 3.2 Create API service layer
    - Create src/services/api.ts with Axios instance
    - Configure base URL from environment variables
    - Implement request/response interceptors for error handling
    - Create API methods for all 9 Lambda endpoints:
      - POST /voice/transcribe
      - POST /transactions
      - GET /transactions/{vendor_id}
      - GET /prices/{item}
      - POST /freshness/classify
      - POST /marketplace/listings
      - GET /marketplace/buyers
      - POST /marketplace/notify
      - GET /trust-score/{vendor_id}
    - Add retry logic for failed requests
    - Implement offline request queueing
    - _Requirements: Backend API integration_
  
  - [ ] 3.3 Create AWS service utilities
    - Create S3 upload utility for images and audio files
    - Implement presigned URL generation for secure uploads
    - Create DynamoDB query utilities (via API Gateway)
    - Add error handling for AWS service failures
    - Implement fallback to demo mode when offline
    - _Requirements: AWS service integration_

- [ ] 4. Implement state management with Redux Toolkit
  - [ ] 4.1 Set up Redux store
    - Install Redux Toolkit and React Redux
    - Create store configuration in src/store/index.ts
    - Set up Redux DevTools for debugging
    - Configure persistence with redux-persist and AsyncStorage
    - _Requirements: State management_
  
  - [ ] 4.2 Create Redux slices
    - Create authSlice for vendor authentication
    - Create transactionsSlice for transaction data
    - Create pricesSlice for market price data
    - Create marketplaceSlice for listings and buyers
    - Create trustScoreSlice for vendor trust score
    - Create uiSlice for loading states and errors
    - Add async thunks for API calls
    - _Requirements: State management_
  
  - [ ] 4.3 Implement offline-first data sync
    - Create sync queue for offline operations
    - Implement background sync when connection restored
    - Add conflict resolution for offline edits
    - Store pending operations in AsyncStorage
    - _Requirements: Offline functionality_

- [x] 5. Implement navigation structure
  - Create navigation container with React Navigation
  - Set up bottom tab navigator with 5 tabs: Home, Prices, Scanner, Marketplace, Profile
  - Create stack navigator for each tab
  - Implement deep linking configuration
  - Add navigation guards for authentication
  - Configure screen transitions and animations
  - Set up navigation types for TypeScript
  - _Requirements: App navigation_

- [ ] 6. Implement Home Dashboard screen
  - [ ] 6.1 Create Home screen UI
    - Create large circular microphone button (60% of screen width)
    - Add animated pulse effect on microphone button
    - Display daily summary cards: total sales, transaction count, today's earnings
    - Add quick access buttons for: Price Check, Scan Produce, Marketplace, Trust Score
    - Implement pull-to-refresh for data sync
    - Add offline indicator banner
    - _Requirements: Home dashboard, mobile UX_
  
  - [ ] 6.2 Implement voice recording functionality
    - Integrate React Native Voice for audio recording
    - Add recording animation with waveform visualization
    - Implement start/stop recording controls
    - Save audio file to device temporary storage
    - Upload audio to S3 via API
    - Display recording duration timer
    - Add permission handling for microphone access
    - _Requirements: Voice recording_
  
  - [ ] 6.3 Connect to voice transcription API
    - Call POST /voice/transcribe with audio file
    - Display transcription result in modal
    - Show confidence score indicator
    - Add retry button for failed transcriptions
    - Implement fallback to text input if voice fails
    - _Requirements: Voice transcription integration_

- [ ] 7. Implement Voice Transaction screen
  - Create transaction recording flow screen
  - Display transcription result with editable fields
  - Show extracted transaction details: item, quantity, unit, price
  - Add manual edit capability for corrections
  - Implement transaction confirmation button
  - Call POST /transactions API to save
  - Display success/error feedback with native alerts
  - Add transaction to local cache immediately
  - Navigate back to Home on success
  - _Requirements: Voice transaction feature_

- [ ] 8. Implement Transaction History screen
  - Create transaction list with FlatList for performance
  - Display transactions with: date, item, quantity, price, total
  - Implement pull-to-refresh to sync from backend
  - Add search/filter by date range and item name
  - Show empty state when no transactions
  - Implement infinite scroll pagination
  - Add swipe-to-delete gesture for transactions
  - Call GET /transactions/{vendor_id} API
  - Cache transactions in Redux and AsyncStorage
  - _Requirements: Transaction history_

- [ ] 9. Implement Price Intelligence screen
  - [ ] 9.1 Create price query interface
    - Add search input with voice button
    - Implement voice-to-text for item search
    - Add recent searches list
    - Display loading skeleton while fetching
    - _Requirements: Price query UI_
  
  - [ ] 9.2 Display price comparison
    - Create price comparison cards for 3 mandis
    - Show mandi name, price, distance, and trend indicator
    - Color code prices: Green (low), Yellow (medium), Red (high)
    - Add price trend arrows (↑↓) compared to yesterday
    - Display distance from vendor location using geolocation
    - Call GET /prices/{item} API
    - Cache price data with 1-hour TTL
    - _Requirements: Price intelligence feature_
  
  - [ ] 9.3 Implement geolocation for distance calculation
    - Request location permissions
    - Get current vendor location
    - Calculate distance to mandis
    - Sort mandis by distance (nearest first)
    - Handle location permission denial gracefully
    - _Requirements: Geolocation integration_

- [ ] 10. Implement Freshness Scanner screen
  - [ ] 10.1 Create camera interface
    - Integrate React Native Camera
    - Create camera view with circular overlay guide
    - Add capture button with animation
    - Implement flash toggle
    - Add gallery picker as alternative to camera
    - Request camera permissions
    - Handle permission denial with fallback
    - _Requirements: Camera integration_
  
  - [ ] 10.2 Implement image capture and upload
    - Capture image from camera
    - Compress image for upload (max 2MB)
    - Upload image to S3 bucket
    - Display upload progress indicator
    - Call POST /freshness/classify API
    - _Requirements: Image upload_
  
  - [ ] 10.3 Display freshness classification result
    - Show classification result: Fresh, B-Grade, or Waste
    - Display color-coded badge (Green/Yellow/Red)
    - Show confidence percentage
    - Display shelf life estimate for Fresh items
    - Show suggestions for B-Grade (juice, pickle) and Waste (compost)
    - Add "List on Marketplace" button for B-Grade items
    - Navigate to marketplace listing form on button press
    - _Requirements: Freshness classification display_

- [ ] 11. Implement Marketplace screen
  - [ ] 11.1 Create listing form
    - Add form fields: item name, weight (kg), price per kg, description
    - Implement image picker for produce photo
    - Add form validation
    - Call POST /marketplace/listings API
    - Display success message on listing creation
    - _Requirements: Marketplace listing creation_
  
  - [ ] 11.2 Display vendor's active listings
    - Create listings grid with images
    - Show listing details: item, weight, price, status
    - Add edit and delete actions
    - Implement pull-to-refresh
    - Call GET /marketplace/listings API (filtered by vendor_id)
    - _Requirements: Marketplace listings display_
  
  - [ ] 11.3 Show nearby buyers
    - Display buyer count and distance
    - Call GET /marketplace/buyers API
    - Show notification status (sent/pending)
    - Add "Notify Buyers" button
    - Call POST /marketplace/notify API
    - _Requirements: Buyer notifications_
  
  - [ ] 11.4 Display Mandi Credits
    - Show Mandi Credits balance prominently
    - Display tier badge (Bronze/Silver/Gold)
    - Show credits earned per transaction
    - Add "How Credits Work" info modal
    - _Requirements: Mandi Credits display_

- [ ] 12. Implement Trust Score Profile screen
  - Create profile header with vendor name and photo
  - Display Trust Score as circular progress indicator
  - Show current score and next tier threshold
  - Display tier badge with icon (Bronze/Silver/Gold)
  - Show score breakdown cards:
    - Transactions completed (+10 each)
    - Marketplace sales (+20 each)
    - Price reports (+5 each)
    - Consistency bonus
  - Add tier benefits list
  - Implement "Share Certificate" button (generate image)
  - Call GET /trust-score/{vendor_id} API
  - Cache trust score data
  - _Requirements: Trust Score feature_

- [ ] 13. Implement authentication and onboarding
  - [ ] 13.1 Create splash screen
    - Design splash screen with app logo
    - Add loading animation
    - Check authentication status
    - Navigate to Login or Home based on auth state
    - _Requirements: App initialization_
  
  - [x] 13.2 Create login screen
    - Add login form: username, password
    - Implement form validation
    - Add "Remember Me" checkbox
    - Store credentials securely in Keychain (iOS) / Keystore (Android)
    - Add demo mode toggle
    - Implement demo credentials: demo_vendor / hackathon2024
    - Navigate to Home on successful login
    - _Requirements: Authentication_
  
  - [ ] 13.3 Create onboarding tutorial
    - Create swipeable tutorial screens (4-5 screens)
    - Explain each feature with illustrations
    - Add "Skip" and "Next" buttons
    - Show tutorial only on first launch
    - Store tutorial completion flag in AsyncStorage
    - _Requirements: User onboarding_

- [ ] 14. Implement offline functionality
  - [ ] 14.1 Create offline detection
    - Monitor network connectivity with NetInfo
    - Display offline banner when disconnected
    - Update UI state based on connectivity
    - _Requirements: Offline detection_
  
  - [ ] 14.2 Implement offline data caching
    - Cache all API responses in AsyncStorage
    - Serve cached data when offline
    - Add cache expiration logic (TTL)
    - Display "cached data" indicator
    - _Requirements: Offline caching_
  
  - [ ] 14.3 Implement offline operation queue
    - Queue write operations when offline (transactions, listings)
    - Store queue in AsyncStorage
    - Sync queue when connection restored
    - Display pending operations count
    - Show sync progress indicator
    - Handle sync failures gracefully
    - _Requirements: Offline operations_

- [ ] 15. Implement demo mode
  - Create demo mode toggle in settings
  - Use mock data for all API calls in demo mode
  - Implement mock responses for all 9 endpoints
  - Store demo data in local JSON files
  - Add "Demo Mode" badge in header
  - Disable actual API calls in demo mode
  - _Requirements: Demo mode for testing_

- [ ] 16. Implement settings and preferences
  - Create settings screen
  - Add language selection (Hindi/English)
  - Add notification preferences
  - Add data sync preferences (WiFi only, Always)
  - Add cache management (Clear cache button)
  - Add logout button
  - Add app version and build number
  - Add "About" section with team info
  - _Requirements: App settings_

- [ ] 17. Implement push notifications
  - [ ] 17.1 Set up Firebase Cloud Messaging (FCM)
    - Create Firebase project
    - Add Firebase to Android app
    - Add Firebase to iOS app
    - Configure FCM in both platforms
    - _Requirements: Push notifications setup_
  
  - [ ] 17.2 Implement notification handling
    - Request notification permissions
    - Register device token with backend
    - Handle foreground notifications
    - Handle background notifications
    - Handle notification tap actions
    - Navigate to relevant screen on notification tap
    - _Requirements: Notification handling_
  
  - [ ] 17.3 Create notification types
    - Price alert notifications
    - Marketplace buyer interest notifications
    - Trust score milestone notifications
    - Transaction reminders
    - _Requirements: Notification types_

- [ ] 18. Optimize performance for low-end devices
  - [ ] 18.1 Implement image optimization
    - Compress images before upload (max 2MB)
    - Use image caching with react-native-fast-image
    - Implement lazy loading for images
    - Use thumbnail versions for lists
    - _Requirements: Performance optimization_
  
  - [ ] 18.2 Optimize list rendering
    - Use FlatList with proper optimization props
    - Implement virtualization for long lists
    - Add pagination for large datasets
    - Use React.memo for list items
    - Optimize re-renders with useMemo and useCallback
    - _Requirements: Performance optimization_
  
  - [ ] 18.3 Reduce bundle size
    - Enable Hermes engine for Android
    - Configure ProGuard for code minification
    - Remove unused dependencies
    - Use dynamic imports for large modules
    - Optimize Metro bundler configuration
    - _Requirements: Bundle size optimization_

- [ ] 19. Implement localization (Hindi + English)
  - Install react-native-localize and i18next
  - Create translation files for Hindi and English
  - Translate all UI strings
  - Implement language switcher in settings
  - Detect device language on first launch
  - Store language preference in AsyncStorage
  - Support RTL layout if needed
  - _Requirements: Multi-language support_

- [ ] 20. Add error handling and logging
  - [ ] 20.1 Implement global error boundary
    - Create error boundary component
    - Display user-friendly error screens
    - Add "Retry" and "Report" buttons
    - Log errors to console in development
    - _Requirements: Error handling_
  
  - [ ] 20.2 Set up crash reporting
    - Integrate Sentry or Firebase Crashlytics
    - Configure error reporting for production
    - Add breadcrumbs for debugging
    - Track user actions before crashes
    - _Requirements: Crash reporting_
  
  - [ ] 20.3 Implement API error handling
    - Handle network errors gracefully
    - Display appropriate error messages
    - Implement retry logic with exponential backoff
    - Show offline message for connectivity issues
    - _Requirements: API error handling_

- [ ] 21. Implement analytics and tracking
  - Integrate Firebase Analytics or AWS Pinpoint
  - Track screen views
  - Track user actions (button clicks, feature usage)
  - Track API call success/failure rates
  - Track offline mode usage
  - Track demo mode usage
  - Add custom events for key features
  - _Requirements: Analytics_

- [ ] 22. Create Android build and release
  - [ ] 22.1 Configure Android release build
    - Generate release keystore
    - Configure signing in android/app/build.gradle
    - Set up ProGuard rules
    - Configure version code and version name
    - _Requirements: Android release_
  
  - [ ] 22.2 Build Android APK/AAB
    - Build release APK: `./gradlew assembleRelease`
    - Build release AAB: `./gradlew bundleRelease`
    - Test APK on physical device
    - Verify all features work in release mode
    - _Requirements: Android build_
  
  - [ ] 22.3 Prepare for Google Play Store
    - Create app listing with screenshots
    - Write app description (English + Hindi)
    - Create feature graphic and icon
    - Set up content rating
    - Configure pricing and distribution
    - Upload AAB to Play Console
    - _Requirements: Play Store submission_

- [ ] 23. Create iOS build and release
  - [ ] 23.1 Configure iOS release build
    - Set up code signing certificates
    - Configure provisioning profiles
    - Set up App Store Connect account
    - Configure version and build number
    - _Requirements: iOS release_
  
  - [ ] 23.2 Build iOS IPA
    - Archive app in Xcode
    - Validate archive
    - Export IPA for App Store distribution
    - Test on physical iOS device
    - Verify all features work in release mode
    - _Requirements: iOS build_
  
  - [ ] 23.3 Prepare for App Store
    - Create app listing with screenshots
    - Write app description (English + Hindi)
    - Create app preview video
    - Set up pricing and availability
    - Submit for App Store review
    - _Requirements: App Store submission_

- [ ] 24. Write comprehensive tests
  - [ ] 24.1 Set up testing framework
    - Install Jest and React Native Testing Library
    - Configure test environment
    - Set up test coverage reporting
    - _Requirements: Testing setup_
  
  - [ ] 24.2 Write unit tests
    - Test Redux slices and reducers
    - Test API service functions
    - Test utility functions
    - Test custom hooks
    - Aim for 80%+ code coverage
    - _Requirements: Unit testing_
  
  - [ ] 24.3 Write integration tests
    - Test navigation flows
    - Test API integration
    - Test offline functionality
    - Test state persistence
    - _Requirements: Integration testing_
  
  - [ ] 24.4 Write E2E tests
    - Install Detox for E2E testing
    - Write E2E tests for critical user flows
    - Test on both Android and iOS
    - _Requirements: E2E testing_

- [ ] 25. Create mobile app documentation
  - [ ] 25.1 Write README for mobile app
    - Add project overview
    - Document prerequisites (Node, React Native CLI, Android Studio, Xcode)
    - Write setup instructions for Android
    - Write setup instructions for iOS
    - Document environment variables
    - Add troubleshooting section
    - _Requirements: Documentation_
  
  - [ ] 25.2 Create development guide
    - Document project structure
    - Explain state management architecture
    - Document API integration
    - Add coding standards and conventions
    - Document build and release process
    - _Requirements: Developer documentation_
  
  - [ ] 25.3 Create user guide
    - Write feature documentation
    - Create user manual with screenshots
    - Document demo mode usage
    - Add FAQ section
    - _Requirements: User documentation_

- [ ] 26. Final testing and QA
  - [ ] 26.1 Test on multiple Android devices
    - Test on Android 5.0 (API 21)
    - Test on Android 13 (API 33)
    - Test on low-end device (2GB RAM)
    - Test on high-end device
    - Test on different screen sizes
    - _Requirements: Android QA_
  
  - [ ] 26.2 Test on multiple iOS devices
    - Test on iOS 12
    - Test on iOS 16
    - Test on iPhone SE (small screen)
    - Test on iPhone 14 Pro Max (large screen)
    - Test on iPad (tablet)
    - _Requirements: iOS QA_
  
  - [ ] 26.3 Test all features end-to-end
    - Test voice transaction flow
    - Test price intelligence
    - Test freshness scanner
    - Test marketplace
    - Test trust score
    - Test offline mode
    - Test demo mode
    - Test notifications
    - _Requirements: Feature QA_
  
  - [ ] 26.4 Performance testing
    - Test app launch time (< 3 seconds)
    - Test screen transition smoothness
    - Test memory usage (< 200MB)
    - Test battery consumption
    - Test network usage
    - _Requirements: Performance QA_

- [ ] 27. Checkpoint - Mobile app ready for release
  - Ensure all tests pass
  - Verify builds work on both platforms
  - Confirm all features functional
  - Ask user if questions arise

## Notes

- Use React Native CLI (not Expo) for full native control
- Prioritize offline-first architecture for reliability
- Optimize for low-end devices (2GB RAM, slow networks)
- Support Hindi and English languages
- Reuse existing AWS backend infrastructure
- Follow platform-specific design guidelines (Material Design for Android, Human Interface Guidelines for iOS)
- Test on real devices, not just emulators
- Implement proper error handling and user feedback
- Use native modules for camera, microphone, and geolocation
- Implement proper permission handling for both platforms
- Follow React Native best practices for performance
- Use TypeScript for type safety
- Implement proper state management with Redux
- Cache data locally for offline access
- Queue operations when offline and sync when online
- Use proper image compression and optimization
- Implement proper navigation with React Navigation
- Follow accessibility guidelines for both platforms
- Test thoroughly on multiple devices and OS versions

## Development Environment Requirements

### General
- Node.js 16+
- npm or yarn
- Git
- React Native CLI
- TypeScript

### Android
- Android Studio
- Android SDK (API 21-33)
- Java JDK 11
- Android Emulator or physical device

### iOS (macOS only)
- Xcode 14+
- CocoaPods
- iOS Simulator or physical device
- Apple Developer account (for device testing and App Store)

## Estimated Timeline

- Project setup: 1-2 days
- Core features implementation: 2-3 weeks
- AWS integration: 3-5 days
- Platform-specific features: 1 week
- Testing and QA: 1 week
- Documentation: 2-3 days
- Build and release: 2-3 days

**Total: 5-7 weeks**

## Success Criteria

- [ ] App runs on Android 5.0+ and iOS 12.0+
- [ ] All 6 features working (Voice, Prices, Scanner, Marketplace, Trust Score)
- [ ] Offline mode functional
- [ ] Demo mode working
- [ ] Performance optimized for 2GB RAM devices
- [ ] Both Android APK and iOS IPA built successfully
- [ ] All tests passing (unit, integration, E2E)
- [ ] Documentation complete
- [ ] Ready for Play Store and App Store submission

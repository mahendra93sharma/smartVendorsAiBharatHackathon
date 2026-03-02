# Requirements: React Native Mobile App (Android & iOS)

## 1. Project Overview

Create native mobile applications for Android and iOS using React Native CLI that replicate all features from the web frontend and connect to the existing AWS backend infrastructure. The apps must be optimized for low-end devices (2GB RAM), support offline functionality, and provide a native mobile user experience.

## 2. User Stories

### 2.1 As a street vendor, I want to use the app on my Android phone
**Acceptance Criteria:**
- App runs on Android 5.0 (API 21) and above
- App works on devices with 2GB RAM
- App installs from APK file
- App size is under 50MB
- App launches in under 3 seconds

### 2.2 As a street vendor, I want to use the app on my iPhone
**Acceptance Criteria:**
- App runs on iOS 12.0 and above
- App works on older iPhone models (iPhone 6s and above)
- App installs from IPA file or App Store
- App follows iOS design guidelines
- App launches in under 3 seconds

### 2.3 As a vendor, I want to record transactions using voice in Hindi
**Acceptance Criteria:**
- App can record audio using device microphone
- App requests microphone permission properly
- Audio is uploaded to AWS S3
- Transcription works for Hindi language
- Extracted transaction data is displayed for confirmation
- Transaction is saved to backend via API

### 2.4 As a vendor, I want to check market prices on my phone
**Acceptance Criteria:**
- App displays prices from 3 mandis
- Prices are color-coded (green/yellow/red)
- Distance to each mandi is shown
- Prices are sorted by distance (nearest first)
- App uses device location for distance calculation
- Price data is cached for offline access

### 2.5 As a vendor, I want to scan produce for freshness using my phone camera
**Acceptance Criteria:**
- App can access device camera
- App requests camera permission properly
- Camera interface has circular overlay guide
- Image is captured and compressed
- Image is uploaded to S3
- Classification result is displayed with color-coded badge
- Shelf life estimate is shown for fresh items
- Suggestions are provided for B-Grade and Waste items

### 2.6 As a vendor, I want to list B-Grade produce on the marketplace
**Acceptance Criteria:**
- App has listing creation form
- Form includes: item name, weight, price, description, photo
- Photo can be taken with camera or selected from gallery
- Listing is created via API
- Listing appears in vendor's active listings
- Nearby buyers are notified

### 2.7 As a vendor, I want to view my Trust Score on my phone
**Acceptance Criteria:**
- Trust Score is displayed as circular progress indicator
- Current tier badge is shown (Bronze/Silver/Gold)
- Score breakdown is displayed
- Next tier threshold is shown
- Certificate can be shared as image

### 2.8 As a vendor, I want to use the app offline
**Acceptance Criteria:**
- App detects offline status
- Offline banner is displayed when disconnected
- Cached data is served when offline
- Write operations are queued when offline
- Queue is synced when connection is restored
- Pending operations count is displayed

### 2.9 As a vendor, I want to use the app in Hindi
**Acceptance Criteria:**
- All UI text is available in Hindi
- Language can be switched in settings
- Device language is detected on first launch
- Language preference is persisted

### 2.10 As a vendor, I want to receive notifications about marketplace activity
**Acceptance Criteria:**
- App requests notification permission
- Push notifications work when app is closed
- Notifications show for: buyer interest, price alerts, trust score milestones
- Tapping notification navigates to relevant screen

## 3. Functional Requirements

### 3.1 Platform Support
- Support Android 5.0 (API 21) and above
- Support iOS 12.0 and above
- Build native apps using React Native CLI (not Expo)
- Support both phone and tablet form factors

### 3.2 Authentication
- Login screen with username and password
- Demo mode with credentials: demo_vendor / hackathon2024
- Secure credential storage (Keychain for iOS, Keystore for Android)
- Remember me functionality
- Logout functionality

### 3.3 Home Dashboard
- Large circular microphone button for voice recording
- Daily summary cards (sales, transactions, earnings)
- Quick access buttons for all features
- Pull-to-refresh for data sync
- Offline indicator banner

### 3.4 Voice Transaction
- Record audio using device microphone
- Upload audio to S3
- Call transcription API
- Display transcription result
- Extract transaction details (item, quantity, price)
- Allow manual editing of extracted data
- Save transaction via API
- Cache transaction locally

### 3.5 Transaction History
- Display list of all transactions
- Show: date, item, quantity, price, total
- Search and filter by date and item
- Pull-to-refresh to sync
- Infinite scroll pagination
- Swipe-to-delete gesture

### 3.6 Price Intelligence
- Search for item prices (voice or text)
- Display prices from 3 mandis
- Show: mandi name, price, distance, trend
- Color-code prices (green/yellow/red)
- Use device location for distance calculation
- Cache price data with 1-hour TTL

### 3.7 Freshness Scanner
- Access device camera
- Capture produce image
- Compress image (max 2MB)
- Upload image to S3
- Call classification API
- Display result: Fresh, B-Grade, or Waste
- Show confidence percentage
- Display shelf life estimate
- Provide suggestions based on category
- Option to list B-Grade items on marketplace

### 3.8 Marketplace
- Create listing form (item, weight, price, description, photo)
- Display vendor's active listings
- Show nearby buyers count
- Notify buyers button
- Display Mandi Credits balance
- Show tier badge

### 3.9 Trust Score Profile
- Display Trust Score as circular progress
- Show current tier badge
- Display score breakdown
- Show next tier threshold
- Share certificate as image

### 3.10 Offline Functionality
- Detect network connectivity
- Cache all API responses
- Serve cached data when offline
- Queue write operations when offline
- Sync queue when connection restored
- Display pending operations count

### 3.11 Settings
- Language selection (Hindi/English)
- Notification preferences
- Data sync preferences (WiFi only, Always)
- Cache management (Clear cache)
- Logout
- App version and build info
- About section

### 3.12 Notifications
- Push notifications via Firebase Cloud Messaging
- Notification types: price alerts, buyer interest, trust score milestones
- Handle foreground and background notifications
- Navigate to relevant screen on tap

## 4. Non-Functional Requirements

### 4.1 Performance
- App launch time: < 3 seconds
- Screen transitions: smooth 60fps
- Memory usage: < 200MB on low-end devices
- Image loading: < 2 seconds
- API response handling: < 1 second
- Offline mode: instant data access from cache

### 4.2 Reliability
- App crash rate: < 0.1%
- API success rate: > 95%
- Offline sync success rate: > 99%
- Data persistence: 100% reliable

### 4.3 Usability
- Intuitive navigation
- Clear visual feedback for all actions
- Error messages in user's language
- Accessible to users with low literacy
- Large touch targets (minimum 44x44 points)
- High contrast for outdoor visibility

### 4.4 Compatibility
- Android: API 21-33 (Android 5.0 - 13)
- iOS: 12.0 - 16.0
- Screen sizes: 4" to 6.7" phones, 7" to 12" tablets
- Low-end devices: 2GB RAM, slow processors
- Network: 2G, 3G, 4G, WiFi

### 4.5 Security
- Secure credential storage
- HTTPS for all API calls
- No sensitive data in logs
- Proper permission handling
- Secure file storage

### 4.6 Scalability
- Support 10,000+ transactions per vendor
- Handle 1000+ marketplace listings
- Efficient data pagination
- Optimized image loading
- Minimal memory footprint

### 4.7 Maintainability
- TypeScript for type safety
- Modular code architecture
- Comprehensive documentation
- Unit and integration tests
- E2E tests for critical flows

## 5. Technical Requirements

### 5.1 Technology Stack
- React Native CLI (latest stable)
- TypeScript
- React Navigation
- Redux Toolkit
- AsyncStorage
- React Native Voice
- React Native Camera
- Axios
- AWS Amplify

### 5.2 AWS Integration
- Connect to existing Lambda functions via API Gateway
- Upload files to existing S3 buckets
- Query existing DynamoDB tables via API
- Use existing AWS Transcribe integration
- Use existing AWS Bedrock integration
- Use existing SageMaker endpoints

### 5.3 Build Configuration
- Android: minSdkVersion 21, targetSdkVersion 33
- iOS: minimum deployment target 12.0
- ProGuard for Android release builds
- Code signing for iOS release builds
- Environment-specific configurations

### 5.4 Testing
- Unit tests with Jest
- Integration tests with React Native Testing Library
- E2E tests with Detox
- Test coverage: > 80%

### 5.5 Code Quality
- ESLint for linting
- Prettier for formatting
- TypeScript strict mode
- Pre-commit hooks
- Code review process

## 6. API Integration Requirements

### 6.1 Backend Endpoints
All endpoints from existing AWS Lambda functions:
- POST /voice/transcribe - Upload audio, get transcription
- POST /transactions - Create transaction
- GET /transactions/{vendor_id} - Get vendor transactions
- GET /prices/{item} - Get market prices
- POST /freshness/classify - Upload image, get classification
- POST /marketplace/listings - Create listing
- GET /marketplace/buyers - Get nearby buyers
- POST /marketplace/notify - Notify buyers
- GET /trust-score/{vendor_id} - Get trust score

### 6.2 API Requirements
- Base URL from environment variable
- Request/response interceptors
- Error handling with retry logic
- Offline request queueing
- Response caching
- Timeout handling (30 seconds)

## 7. Localization Requirements

### 7.1 Languages
- English (en)
- Hindi (hi)

### 7.2 Localization Scope
- All UI text
- Error messages
- Validation messages
- Notification messages
- Date and time formats
- Number formats (currency)

## 8. Accessibility Requirements

### 8.1 Visual
- High contrast mode support
- Large text support
- Color-blind friendly color schemes
- Minimum touch target size: 44x44 points

### 8.2 Audio
- Voice feedback for critical actions
- Audio alternatives for visual content

### 8.3 Navigation
- Keyboard navigation support (Android)
- VoiceOver support (iOS)
- TalkBack support (Android)

## 9. Analytics Requirements

### 9.1 Events to Track
- Screen views
- Feature usage (voice, scanner, marketplace, etc.)
- API call success/failure rates
- Offline mode usage
- Demo mode usage
- Error occurrences
- User retention

### 9.2 Analytics Platform
- Firebase Analytics or AWS Pinpoint
- Custom event tracking
- User property tracking
- Crash reporting with Sentry or Firebase Crashlytics

## 10. Release Requirements

### 10.1 Android Release
- Signed APK for direct distribution
- Signed AAB for Google Play Store
- App listing with screenshots
- Feature graphic and icon
- App description (English + Hindi)
- Content rating
- Privacy policy

### 10.2 iOS Release
- Signed IPA for App Store
- App listing with screenshots
- App preview video
- App description (English + Hindi)
- Content rating
- Privacy policy
- App Store review submission

## 11. Documentation Requirements

### 11.1 Developer Documentation
- README with setup instructions
- Architecture documentation
- API integration guide
- Build and release guide
- Troubleshooting guide

### 11.2 User Documentation
- User manual with screenshots
- Feature documentation
- FAQ
- Demo mode guide

## 12. Success Metrics

### 12.1 Technical Metrics
- App launch time: < 3 seconds
- Crash rate: < 0.1%
- API success rate: > 95%
- Test coverage: > 80%
- App size: < 50MB

### 12.2 User Metrics
- User retention: > 70% after 7 days
- Feature adoption: > 60% for each feature
- Offline mode usage: > 30% of sessions
- Average session duration: > 5 minutes

### 12.3 Business Metrics
- App Store rating: > 4.0 stars
- Play Store rating: > 4.0 stars
- Daily active users: > 1000
- Transaction volume: > 10,000 per month

## 13. Constraints

### 13.1 Technical Constraints
- Must use React Native CLI (not Expo)
- Must connect to existing AWS backend
- Must support Android 5.0+ and iOS 12.0+
- Must work on 2GB RAM devices
- Must support offline mode

### 13.2 Business Constraints
- Development timeline: 5-7 weeks
- Budget: Minimal (use free tools and services)
- Team size: 1-3 developers

### 13.3 Platform Constraints
- Android: Google Play Store policies
- iOS: App Store Review Guidelines
- Both: Privacy and data protection regulations

## 14. Assumptions

- Existing AWS backend is stable and accessible
- API Gateway endpoints are properly configured
- S3 buckets have correct permissions
- DynamoDB tables are properly indexed
- Lambda functions handle mobile requests
- Network connectivity is available most of the time
- Users have basic smartphone literacy
- Users grant necessary permissions (camera, microphone, location)

## 15. Dependencies

- Existing AWS infrastructure (Lambda, S3, DynamoDB)
- API Gateway endpoints
- Firebase project for push notifications
- Apple Developer account (for iOS)
- Google Play Console account (for Android)
- Physical devices for testing
- macOS machine for iOS development

## 16. Risks and Mitigations

### 16.1 Technical Risks
- **Risk:** React Native version compatibility issues
  - **Mitigation:** Use stable LTS version, test thoroughly
- **Risk:** Native module linking failures
  - **Mitigation:** Follow official documentation, test on clean install
- **Risk:** Performance issues on low-end devices
  - **Mitigation:** Optimize early, test on target devices

### 16.2 Platform Risks
- **Risk:** App Store rejection
  - **Mitigation:** Follow guidelines strictly, prepare for review
- **Risk:** Permission denial by users
  - **Mitigation:** Implement graceful fallbacks, explain permissions clearly

### 16.3 Integration Risks
- **Risk:** AWS backend changes breaking mobile app
  - **Mitigation:** Version API endpoints, implement error handling
- **Risk:** Network connectivity issues
  - **Mitigation:** Implement robust offline mode

## 17. Future Enhancements

- WhatsApp integration for notifications
- Biometric authentication (fingerprint, face ID)
- Multi-vendor collaboration features
- Advanced analytics dashboard
- Voice commands for navigation
- AR features for produce scanning
- Blockchain integration for trust score
- Integration with payment gateways
- Multi-language support (more Indian languages)
- Tablet-optimized UI

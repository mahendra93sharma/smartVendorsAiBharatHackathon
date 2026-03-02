# Design Document: React Native Mobile App (Android & iOS)

## Overview

This design document describes the architecture and implementation approach for native mobile applications (Android and iOS) built with React Native CLI. The apps replicate all features from the web frontend while providing native mobile UX patterns optimized for low-end devices (2GB RAM). The architecture follows an offline-first approach with robust AWS backend integration.

### Key Design Principles

1. **Offline-First**: All data is cached locally; operations queue when offline and sync when connected
2. **Performance**: Optimized for 2GB RAM devices with lazy loading, image compression, and efficient rendering
3. **Native Experience**: Platform-specific UI patterns following Material Design (Android) and Human Interface Guidelines (iOS)
4. **Modular Architecture**: Clear separation between UI, business logic, state management, and API integration
5. **Type Safety**: TypeScript throughout for compile-time error detection
6. **Testability**: Designed for comprehensive unit, integration, and property-based testing

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React Native App                         │
├─────────────────────────────────────────────────────────────┤
│  Presentation Layer (Screens & Components)                   │
│    ├─ Home Dashboard                                         │
│    ├─ Voice Transaction                                      │
│    ├─ Transaction History                                    │
│    ├─ Price Intelligence                                     │
│    ├─ Freshness Scanner                                      │
│    ├─ Marketplace                                            │
│    └─ Trust Score Profile                                    │
├─────────────────────────────────────────────────────────────┤
│  State Management Layer (Redux Toolkit)                      │
│    ├─ Auth Slice                                             │
│    ├─ Transactions Slice                                     │
│    ├─ Prices Slice                                           │
│    ├─ Marketplace Slice                                      │
│    ├─ Trust Score Slice                                      │
│    └─ UI Slice (loading, errors, offline status)            │
├─────────────────────────────────────────────────────────────┤
│  Business Logic Layer                                        │
│    ├─ Offline Queue Manager                                  │
│    ├─ Cache Manager (TTL, invalidation)                      │
│    ├─ Permission Manager                                     │
│    ├─ Location Service                                       │
│    └─ Notification Service                                   │
├─────────────────────────────────────────────────────────────┤
│  API Integration Layer                                       │
│    ├─ API Client (Axios)                                     │
│    ├─ Request/Response Interceptors                          │
│    ├─ Retry Logic                                            │
│    └─ Error Handling                                         │
├─────────────────────────────────────────────────────────────┤
│  AWS Services Layer                                          │
│    ├─ S3 Upload Service                                      │
│    ├─ API Gateway Client                                     │
│    └─ Amplify Configuration                                  │
├─────────────────────────────────────────────────────────────┤
│  Native Modules Layer                                        │
│    ├─ Camera (React Native Camera)                           │
│    ├─ Voice Recording (React Native Voice)                   │
│    ├─ Geolocation (React Native Geolocation)                 │
│    ├─ Secure Storage (Keychain/Keystore)                     │
│    └─ Push Notifications (FCM)                               │
├─────────────────────────────────────────────────────────────┤
│  Persistence Layer                                           │
│    ├─ AsyncStorage (key-value store)                         │
│    ├─ Redux Persist                                          │
│    └─ File System (temporary files)                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              AWS Backend Infrastructure                      │
│  ├─ API Gateway (9 endpoints)                                │
│  ├─ Lambda Functions (business logic)                        │
│  ├─ DynamoDB (data storage)                                  │
│  ├─ S3 (audio/image storage)                                 │
│  ├─ AWS Transcribe (Hindi voice-to-text)                     │
│  ├─ AWS Bedrock (LLM for transaction extraction)             │
│  └─ SageMaker (freshness classification)                     │
└─────────────────────────────────────────────────────────────┘
```

### Architecture Patterns

**1. Offline-First Pattern**
- All API responses cached in AsyncStorage with TTL
- Write operations queued when offline
- Background sync when connectivity restored
- Optimistic UI updates for better UX

**2. Repository Pattern**
- API layer abstracts backend communication
- Services provide business logic
- Redux slices manage state
- Components consume state via hooks

**3. Component Composition**
- Atomic design: atoms (buttons, inputs) → molecules (cards) → organisms (lists) → screens
- Reusable components across screens
- Platform-specific components when needed

**4. State Management Pattern**
- Redux Toolkit for global state
- Local component state for UI-only concerns
- Redux Persist for state hydration
- Async thunks for side effects

## Components and Interfaces

### Core Components

#### 1. Navigation Components

**AppNavigator**
- Root navigator managing authentication flow
- Switches between AuthStack and MainStack based on auth state

**MainTabNavigator**
- Bottom tab navigator with 5 tabs
- Tabs: Home, Prices, Scanner, Marketplace, Profile
- Custom tab bar with icons and labels

**Stack Navigators**
- HomeStack: Home → VoiceTransaction → TransactionDetail
- PricesStack: PriceSearch → PriceComparison
- ScannerStack: Camera → ClassificationResult → MarketplaceListing
- MarketplaceStack: Listings → ListingDetail → CreateListing
- ProfileStack: TrustScore → Settings → About

#### 2. Screen Components

**HomeScreen**
- Large circular microphone button (animated)
- Daily summary cards (sales, transactions, earnings)
- Quick access buttons grid
- Pull-to-refresh functionality
- Offline banner

**VoiceTransactionScreen**
- Recording interface with waveform animation
- Transcription display
- Editable transaction fields
- Confirmation button
- Error handling

**TransactionHistoryScreen**
- FlatList with virtualization
- Transaction cards with swipe-to-delete
- Search and filter controls
- Infinite scroll pagination
- Empty state

**PriceIntelligenceScreen**
- Search input with voice button
- Price comparison cards (3 mandis)
- Color-coded pricing
- Distance indicators
- Trend arrows

**FreshnessScannerScreen**
- Camera view with circular overlay
- Capture button with animation
- Gallery picker option
- Classification result display
- Action buttons based on result

**MarketplaceScreen**
- Listing creation form
- Active listings grid
- Nearby buyers display
- Mandi Credits balance
- Notification controls

**TrustScoreScreen**
- Circular progress indicator
- Tier badge display
- Score breakdown cards
- Share certificate button

**SettingsScreen**
- Language selector
- Notification preferences
- Data sync options
- Cache management
- Logout button

#### 3. Reusable UI Components

**Button**
- Primary, secondary, outline variants
- Loading state
- Disabled state
- Icon support

**Card**
- Container with shadow/elevation
- Header, body, footer sections
- Pressable variant

**Input**
- Text input with label
- Error message display
- Icon support
- Validation state

**Badge**
- Color variants (success, warning, error, info)
- Size variants (small, medium, large)
- Icon support

**ProgressCircle**
- Animated circular progress
- Percentage display
- Color customization

**OfflineBanner**
- Sticky banner at top
- Connection status indicator
- Pending operations count

### Service Interfaces

#### APIService

```typescript
interface APIService {
  // Voice & Transcription
  transcribeAudio(audioFile: File): Promise<TranscriptionResponse>;
  
  // Transactions
  createTransaction(transaction: TransactionInput): Promise<Transaction>;
  getTransactions(vendorId: string, page: number): Promise<TransactionPage>;
  deleteTransaction(transactionId: string): Promise<void>;
  
  // Prices
  getPrices(item: string, location: Location): Promise<PriceComparison>;
  
  // Freshness
  classifyFreshness(imageFile: File): Promise<ClassificationResult>;
  
  // Marketplace
  createListing(listing: ListingInput): Promise<Listing>;
  getListings(vendorId: string): Promise<Listing[]>;
  getBuyersNearby(location: Location): Promise<Buyer[]>;
  notifyBuyers(listingId: string): Promise<NotificationResult>;
  
  // Trust Score
  getTrustScore(vendorId: string): Promise<TrustScore>;
}
```

#### S3Service

```typescript
interface S3Service {
  uploadAudio(audioFile: File, vendorId: string): Promise<S3UploadResult>;
  uploadImage(imageFile: File, vendorId: string): Promise<S3UploadResult>;
  getPresignedUrl(key: string): Promise<string>;
}
```

#### CacheService

```typescript
interface CacheService {
  get<T>(key: string): Promise<T | null>;
  set<T>(key: string, value: T, ttl?: number): Promise<void>;
  remove(key: string): Promise<void>;
  clear(): Promise<void>;
  isExpired(key: string): Promise<boolean>;
}
```

#### OfflineQueueService

```typescript
interface OfflineQueueService {
  enqueue(operation: QueuedOperation): Promise<void>;
  dequeue(): Promise<QueuedOperation | null>;
  getQueue(): Promise<QueuedOperation[]>;
  sync(): Promise<SyncResult>;
  clear(): Promise<void>;
}
```

#### PermissionService

```typescript
interface PermissionService {
  requestCamera(): Promise<PermissionStatus>;
  requestMicrophone(): Promise<PermissionStatus>;
  requestLocation(): Promise<PermissionStatus>;
  requestNotifications(): Promise<PermissionStatus>;
  checkPermission(type: PermissionType): Promise<PermissionStatus>;
}
```

#### LocationService

```typescript
interface LocationService {
  getCurrentLocation(): Promise<Location>;
  calculateDistance(from: Location, to: Location): number;
  watchLocation(callback: (location: Location) => void): WatchId;
  clearWatch(watchId: WatchId): void;
}
```

#### NotificationService

```typescript
interface NotificationService {
  initialize(): Promise<void>;
  requestPermission(): Promise<boolean>;
  getToken(): Promise<string>;
  onNotification(callback: (notification: Notification) => void): Unsubscribe;
  onNotificationOpened(callback: (notification: Notification) => void): Unsubscribe;
  displayLocalNotification(notification: LocalNotification): Promise<void>;
}
```

## Data Models

### Core Data Types

```typescript
// Authentication
interface Vendor {
  id: string;
  username: string;
  name: string;
  phone: string;
  location: Location;
  language: 'en' | 'hi';
  createdAt: string;
}

interface AuthState {
  vendor: Vendor | null;
  isAuthenticated: boolean;
  token: string | null;
  isDemoMode: boolean;
}

// Location
interface Location {
  latitude: number;
  longitude: number;
}

// Transactions
interface Transaction {
  id: string;
  vendorId: string;
  item: string;
  quantity: number;
  unit: string;
  pricePerUnit: number;
  totalPrice: number;
  timestamp: string;
  source: 'voice' | 'manual';
  audioUrl?: string;
  transcription?: string;
}

interface TransactionInput {
  vendorId: string;
  item: string;
  quantity: number;
  unit: string;
  pricePerUnit: number;
  source: 'voice' | 'manual';
  audioUrl?: string;
  transcription?: string;
}

interface TransactionPage {
  transactions: Transaction[];
  nextPage: number | null;
  hasMore: boolean;
}

// Voice & Transcription
interface TranscriptionResponse {
  transcription: string;
  confidence: number;
  extractedData: {
    item: string;
    quantity: number;
    unit: string;
    price: number;
  };
}

// Prices
interface PriceData {
  mandiName: string;
  location: Location;
  price: number;
  unit: string;
  trend: 'up' | 'down' | 'stable';
  trendPercentage: number;
  distance: number;
  category: 'low' | 'medium' | 'high';
}

interface PriceComparison {
  item: string;
  timestamp: string;
  prices: PriceData[];
}

// Freshness Classification
interface ClassificationResult {
  category: 'Fresh' | 'B-Grade' | 'Waste';
  confidence: number;
  shelfLife?: number;
  suggestions: string[];
  imageUrl: string;
}

// Marketplace
interface Listing {
  id: string;
  vendorId: string;
  item: string;
  weight: number;
  pricePerKg: number;
  description: string;
  imageUrl: string;
  status: 'active' | 'sold' | 'expired';
  createdAt: string;
  expiresAt: string;
}

interface ListingInput {
  vendorId: string;
  item: string;
  weight: number;
  pricePerKg: number;
  description: string;
  imageFile: File;
}

interface Buyer {
  id: string;
  name: string;
  location: Location;
  distance: number;
}

interface NotificationResult {
  notifiedCount: number;
  success: boolean;
}

// Trust Score
interface TrustScore {
  vendorId: string;
  score: number;
  tier: 'Bronze' | 'Silver' | 'Gold';
  breakdown: {
    transactionsCompleted: number;
    marketplaceSales: number;
    priceReports: number;
    consistencyBonus: number;
  };
  nextTierThreshold: number;
  mandiCredits: number;
}

// Offline Queue
interface QueuedOperation {
  id: string;
  type: 'transaction' | 'listing' | 'notification';
  payload: any;
  timestamp: string;
  retryCount: number;
}

interface SyncResult {
  successful: number;
  failed: number;
  errors: string[];
}

// Cache
interface CacheEntry<T> {
  data: T;
  timestamp: number;
  ttl: number;
}

// Notifications
interface Notification {
  id: string;
  title: string;
  body: string;
  type: 'price_alert' | 'buyer_interest' | 'trust_milestone';
  data: any;
  timestamp: string;
}

// S3 Upload
interface S3UploadResult {
  key: string;
  url: string;
  bucket: string;
}

// Permissions
type PermissionType = 'camera' | 'microphone' | 'location' | 'notifications';
type PermissionStatus = 'granted' | 'denied' | 'blocked' | 'unavailable';
```

### Redux State Shape

```typescript
interface RootState {
  auth: {
    vendor: Vendor | null;
    isAuthenticated: boolean;
    token: string | null;
    isDemoMode: boolean;
  };
  transactions: {
    items: Transaction[];
    currentPage: number;
    hasMore: boolean;
    loading: boolean;
    error: string | null;
  };
  prices: {
    currentItem: string | null;
    comparison: PriceComparison | null;
    loading: boolean;
    error: string | null;
    cachedAt: string | null;
  };
  marketplace: {
    listings: Listing[];
    buyers: Buyer[];
    credits: number;
    loading: boolean;
    error: string | null;
  };
  trustScore: {
    score: TrustScore | null;
    loading: boolean;
    error: string | null;
  };
  ui: {
    isOffline: boolean;
    pendingOperations: number;
    isSyncing: boolean;
    language: 'en' | 'hi';
  };
}
```


## Component Design Details

### 1. API Client Implementation

The API client uses Axios with interceptors for consistent error handling, retry logic, and offline queueing.

**Request Interceptor**:
- Adds authentication token to headers
- Adds request timestamp
- Checks offline status and queues if needed
- Logs requests in development mode

**Response Interceptor**:
- Caches successful responses
- Handles common error codes (401, 403, 404, 500)
- Implements exponential backoff retry (3 attempts)
- Transforms error messages to user-friendly format
- Logs responses in development mode

**Retry Logic**:
- Retry on network errors and 5xx status codes
- Exponential backoff: 1s, 2s, 4s
- Maximum 3 retry attempts
- Skip retry for 4xx errors (except 429)

### 2. Offline Queue Manager

Manages operations when device is offline, ensuring data integrity and eventual consistency.

**Queue Operations**:
- Enqueue: Add operation to queue with timestamp and payload
- Dequeue: Remove and return next operation
- Sync: Process all queued operations when online
- Clear: Remove all operations (after successful sync)

**Sync Strategy**:
- Triggered on connectivity change (offline → online)
- Processes operations in FIFO order
- Retries failed operations up to 3 times
- Removes successful operations from queue
- Persists failed operations for manual review

**Conflict Resolution**:
- Timestamp-based: latest write wins
- User notification for conflicts
- Manual resolution option in settings

### 3. Cache Manager

Manages local data caching with TTL and invalidation strategies.

**Cache Strategy**:
- Transactions: 24-hour TTL
- Prices: 1-hour TTL
- Trust Score: 6-hour TTL
- Marketplace Listings: 30-minute TTL
- Images: 7-day TTL

**Cache Invalidation**:
- Automatic on TTL expiration
- Manual via pull-to-refresh
- On successful write operations
- On user logout

**Storage Limits**:
- Maximum cache size: 100MB
- LRU eviction when limit reached
- User-initiated cache clear in settings

### 4. Permission Manager

Handles runtime permissions for camera, microphone, location, and notifications.

**Permission Flow**:
1. Check current permission status
2. If not granted, show rationale dialog
3. Request permission from OS
4. Handle result (granted/denied/blocked)
5. Provide fallback if denied

**Rationale Messages**:
- Camera: "We need camera access to scan produce freshness"
- Microphone: "We need microphone access to record voice transactions"
- Location: "We need location to show nearby mandi prices"
- Notifications: "Enable notifications to get price alerts and buyer interest"

**Fallback Strategies**:
- Camera denied: Allow gallery picker
- Microphone denied: Provide text input
- Location denied: Manual location entry
- Notifications denied: In-app alerts only

### 5. Location Service

Provides geolocation functionality with distance calculation.

**Location Acquisition**:
- Request high-accuracy location
- Timeout after 10 seconds
- Fallback to last known location
- Cache location for 5 minutes

**Distance Calculation**:
- Haversine formula for great-circle distance
- Returns distance in kilometers
- Rounds to 1 decimal place

### 6. Notification Service

Manages push notifications via Firebase Cloud Messaging.

**Notification Types**:
- Price Alerts: When item price drops below threshold
- Buyer Interest: When buyer views listing
- Trust Milestone: When vendor reaches new tier

**Notification Handling**:
- Foreground: Display in-app banner
- Background: OS notification
- Tap action: Navigate to relevant screen with deep linking

**Token Management**:
- Register device token on login
- Update token on refresh
- Unregister token on logout

### 7. Image Compression Service

Optimizes images before upload to reduce bandwidth and storage.

**Compression Strategy**:
- Target size: < 2MB
- Quality: 80% JPEG
- Max dimensions: 1920x1080
- Preserve aspect ratio
- Strip EXIF data (except orientation)

### 8. Voice Recording Service

Manages audio recording with platform-specific implementations.

**Recording Configuration**:
- Format: AAC (iOS), AMR (Android)
- Sample rate: 16kHz
- Channels: Mono
- Bitrate: 32kbps
- Max duration: 60 seconds

**Recording Flow**:
1. Check microphone permission
2. Initialize audio session
3. Start recording
4. Display waveform animation
5. Stop recording on button press or timeout
6. Save to temporary file
7. Return file path

### 9. Secure Storage Service

Stores sensitive data using platform-specific secure storage.

**Storage Mechanism**:
- iOS: Keychain Services
- Android: EncryptedSharedPreferences (Keystore)

**Stored Data**:
- Authentication token
- Vendor credentials (if "Remember Me" enabled)
- API keys
- Device token

**Security Measures**:
- Encryption at rest
- Biometric protection option
- Auto-clear on app uninstall

## Data Flow Diagrams

### Voice Transaction Flow

```
User → Press Mic Button → Request Permission → Start Recording
  → Display Waveform → Stop Recording → Save Audio File
  → Upload to S3 → Call Transcribe API → Display Result
  → Extract Transaction Data → Show Editable Form
  → User Confirms → Call Create Transaction API
  → Save to Redux → Cache Locally → Queue if Offline
  → Display Success → Navigate to History
```

### Offline Operation Flow

```
User Action → Check Connectivity
  ├─ Online → Call API → Update State → Cache Response
  └─ Offline → Queue Operation → Update State Optimistically
                → Display Offline Banner → Show Pending Count
                
Connectivity Restored → Trigger Sync → Process Queue
  → For Each Operation:
      ├─ Success → Remove from Queue → Update State
      └─ Failure → Increment Retry → Keep in Queue
  → Display Sync Result → Update Pending Count
```

### Price Intelligence Flow

```
User → Enter Item Name (or Voice) → Call Prices API
  → Check Cache (1-hour TTL)
      ├─ Cache Hit → Return Cached Data
      └─ Cache Miss → Fetch from API → Cache Response
  → Get Current Location → Calculate Distances
  → Sort by Distance → Categorize Prices (low/medium/high)
  → Display Comparison Cards → Color Code Results
```

### Freshness Scanner Flow

```
User → Open Scanner → Request Camera Permission
  → Show Camera View → Display Circular Overlay
  → Capture Image → Compress Image (< 2MB)
  → Upload to S3 → Call Classification API
  → Display Result (Fresh/B-Grade/Waste)
  → Show Confidence & Shelf Life → Display Suggestions
  → If B-Grade → Show "List on Marketplace" Button
      → Navigate to Listing Form → Pre-fill Item Name
```


## API Integration Design

### Endpoint Mapping

All endpoints connect to existing AWS Lambda functions via API Gateway:

| Feature | Method | Endpoint | Request | Response |
|---------|--------|----------|---------|----------|
| Voice Transcription | POST | /voice/transcribe | Audio file (S3 key) | TranscriptionResponse |
| Create Transaction | POST | /transactions | TransactionInput | Transaction |
| Get Transactions | GET | /transactions/{vendor_id} | Query params (page, limit) | TransactionPage |
| Get Prices | GET | /prices/{item} | Query params (lat, lon) | PriceComparison |
| Classify Freshness | POST | /freshness/classify | Image file (S3 key) | ClassificationResult |
| Create Listing | POST | /marketplace/listings | ListingInput | Listing |
| Get Buyers | GET | /marketplace/buyers | Query params (lat, lon) | Buyer[] |
| Notify Buyers | POST | /marketplace/notify | Listing ID | NotificationResult |
| Get Trust Score | GET | /trust-score/{vendor_id} | - | TrustScore |

### Request/Response Format

**Standard Request Headers**:
```typescript
{
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${token}`,
  'X-Client-Version': '1.0.0',
  'X-Platform': 'android' | 'ios',
  'X-Device-Id': deviceId
}
```

**Standard Response Format**:
```typescript
{
  success: boolean;
  data: T;
  error?: {
    code: string;
    message: string;
  };
  timestamp: string;
}
```

**Error Codes**:
- 400: Bad Request (validation error)
- 401: Unauthorized (invalid token)
- 403: Forbidden (insufficient permissions)
- 404: Not Found (resource doesn't exist)
- 429: Too Many Requests (rate limit)
- 500: Internal Server Error
- 503: Service Unavailable

### AWS Service Integration

**S3 Upload Flow**:
1. Generate unique key: `{vendorId}/{type}/{timestamp}_{uuid}.{ext}`
2. Compress file if needed (images < 2MB, audio < 1MB)
3. Upload to S3 bucket using AWS Amplify Storage
4. Return S3 key and presigned URL
5. Pass S3 key to Lambda function for processing

**API Gateway Configuration**:
- Base URL from environment variable
- Timeout: 30 seconds
- Retry policy: 3 attempts with exponential backoff
- CORS enabled for mobile origins

**Demo Mode**:
- All API calls return mock data
- No actual AWS service calls
- Mock data stored in src/mocks/
- Simulates network delays (500ms-1s)

## Performance Optimization

### Memory Management

**Target**: < 200MB memory usage on 2GB RAM devices

**Strategies**:
1. Image optimization: Compress, resize, lazy load
2. List virtualization: FlatList with proper props
3. Component memoization: React.memo, useMemo, useCallback
4. State cleanup: Clear unused data from Redux
5. Cache limits: Maximum 100MB, LRU eviction

### Rendering Performance

**Target**: 60fps screen transitions

**Strategies**:
1. Use native driver for animations
2. Avoid inline function definitions in render
3. Optimize FlatList with getItemLayout
4. Use InteractionManager for heavy operations
5. Debounce search inputs
6. Throttle scroll events

### Bundle Size Optimization

**Target**: < 50MB app size

**Strategies**:
1. Enable Hermes engine (Android)
2. ProGuard minification (Android)
3. Remove unused dependencies
4. Dynamic imports for large modules
5. Optimize images and assets
6. Use vector icons instead of PNGs

### Network Optimization

**Strategies**:
1. Cache all API responses
2. Compress request/response payloads
3. Batch API calls when possible
4. Use pagination for large datasets
5. Prefetch data on WiFi
6. Compress images before upload

### Launch Time Optimization

**Target**: < 3 seconds

**Strategies**:
1. Lazy load non-critical screens
2. Defer analytics initialization
3. Use splash screen during initialization
4. Preload critical data only
5. Optimize native module initialization

## Error Handling

### Error Categories

**1. Network Errors**
- No internet connection
- Request timeout
- DNS resolution failure
- SSL/TLS errors

**Handling**: Display offline banner, queue operation, retry when online

**2. API Errors**
- 4xx client errors (validation, auth)
- 5xx server errors
- Rate limiting (429)

**Handling**: Display user-friendly message, provide retry option, log for debugging

**3. Permission Errors**
- Camera denied
- Microphone denied
- Location denied
- Notifications denied

**Handling**: Show rationale, provide fallback, guide to settings

**4. AWS Service Errors**
- S3 upload failure
- Transcription failure
- Classification failure

**Handling**: Retry with backoff, fallback to manual input, display error message

**5. Data Errors**
- Invalid data format
- Missing required fields
- Type mismatches

**Handling**: Validate before submission, display field-level errors, prevent submission

### Error Recovery Strategies

**Automatic Recovery**:
- Retry with exponential backoff
- Fallback to cached data
- Queue for later sync
- Switch to demo mode

**User-Initiated Recovery**:
- Pull-to-refresh
- Retry button
- Clear cache
- Logout and re-login

**Error Logging**:
- Log all errors to console (development)
- Send crash reports to Sentry/Crashlytics (production)
- Include context: user action, app state, device info
- Respect user privacy (no PII in logs)


## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Property Reflection

After analyzing all acceptance criteria, I identified the following testable properties. Some criteria were combined to eliminate redundancy:

- Audio recording and S3 upload can be combined into a single round-trip property
- Permission requests follow a common pattern across all permission types
- Cache retrieval and offline data serving are the same underlying property
- Language translation completeness is a single property across all UI strings

### Properties

**Property 1: Audio recording produces valid files**
*For any* recording session, starting and stopping the recording should produce a valid audio file with non-zero size and correct format (AAC for iOS, AMR for Android).
**Validates: Requirements 2.3.1**

**Property 2: Permission requests handle all outcomes**
*For any* permission type (camera, microphone, location, notifications), requesting permission should return one of the valid statuses (granted, denied, blocked, unavailable) and the app should handle each appropriately.
**Validates: Requirements 2.3.2, 2.5.2, 2.10.1**

**Property 3: S3 upload round-trip**
*For any* valid file (audio or image), uploading to S3 should return a valid S3 key and URL, and the file should be retrievable from that URL.
**Validates: Requirements 2.3.3, 2.5.5**

**Property 4: Transcription API returns structured data**
*For any* valid audio file uploaded to S3, calling the transcription API should return a response containing transcription text, confidence score, and extracted transaction data fields.
**Validates: Requirements 2.3.4, 2.3.5**

**Property 5: Transaction creation is idempotent**
*For any* valid transaction input, creating the transaction via API should return a transaction object with a unique ID, and creating the same transaction twice should not create duplicates.
**Validates: Requirements 2.3.6**

**Property 6: Price comparison contains exactly 3 mandis**
*For any* item price query, the response should contain exactly 3 mandi price entries, each with name, price, location, and distance.
**Validates: Requirements 2.4.1, 2.4.3**

**Property 7: Price categorization is exhaustive and exclusive**
*For any* price value, the categorization function should assign it to exactly one category (low, medium, or high) based on the comparison with other prices.
**Validates: Requirements 2.4.2**

**Property 8: Distance sorting is monotonic**
*For any* list of prices with distances, sorting by distance should produce a list where each distance is less than or equal to the next distance.
**Validates: Requirements 2.4.4**

**Property 9: Distance calculation is positive and symmetric**
*For any* two valid locations, calculating the distance should return a positive number, and the distance from A to B should equal the distance from B to A.
**Validates: Requirements 2.4.5**

**Property 10: Cache retrieval preserves data**
*For any* API response, after caching it, retrieving from cache (even when offline) should return data equivalent to the original response.
**Validates: Requirements 2.4.6, 2.8.3**

**Property 11: Image compression maintains quality constraints**
*For any* captured image, compressing it should produce an image under 2MB while maintaining reasonable quality (JPEG quality >= 80%).
**Validates: Requirements 2.5.4**

**Property 12: Classification results have valid categories**
*For any* image classification response, the category should be one of "Fresh", "B-Grade", or "Waste", and confidence should be between 0 and 100.
**Validates: Requirements 2.5.6**

**Property 13: Fresh items include shelf life**
*For any* classification result with category "Fresh", the result should include a shelf life value greater than 0.
**Validates: Requirements 2.5.7**

**Property 14: Non-fresh items include suggestions**
*For any* classification result with category "B-Grade" or "Waste", the suggestions array should be non-empty.
**Validates: Requirements 2.5.8**

**Property 15: Listing validation enforces required fields**
*For any* listing submission, all required fields (item name, weight, price, description, photo) must be present and valid, or the submission should be rejected.
**Validates: Requirements 2.6.2**

**Property 16: Created listings are retrievable**
*For any* listing created via API, querying the vendor's listings should include that listing with matching data.
**Validates: Requirements 2.6.4, 2.6.5**

**Property 17: Buyer notification returns count**
*For any* listing, calling the notify buyers API should return a success status and a non-negative count of notified buyers.
**Validates: Requirements 2.6.6**

**Property 18: Trust score tier is valid**
*For any* trust score, the tier should be one of "Bronze", "Silver", or "Gold", and should correspond to the score value according to tier thresholds.
**Validates: Requirements 2.7.2**

**Property 19: Next tier threshold is achievable**
*For any* trust score that is not at the maximum tier, the next tier threshold should be greater than the current score.
**Validates: Requirements 2.7.4**

**Property 20: Certificate generation produces valid image**
*For any* trust score, generating a certificate should produce a valid image file (PNG or JPEG) with non-zero size.
**Validates: Requirements 2.7.5**

**Property 21: Connectivity detection reflects actual state**
*For any* network connectivity change, the app's offline status should update to match the actual connectivity state within 1 second.
**Validates: Requirements 2.8.1**

**Property 22: Offline operations are queued**
*For any* write operation (transaction, listing) performed while offline, the operation should be added to the queue and the pending count should increase by 1.
**Validates: Requirements 2.8.4**

**Property 23: Queue sync processes all operations**
*For any* non-empty queue, when connectivity is restored and sync is triggered, all operations should be attempted, and successful operations should be removed from the queue.
**Validates: Requirements 2.8.5**

**Property 24: Translation completeness**
*For any* UI string key in the English translation file, there should be a corresponding entry in the Hindi translation file.
**Validates: Requirements 2.9.1**

**Property 25: Language persistence across restarts**
*For any* language selection, after saving the preference and restarting the app, the app should initialize with the same language.
**Validates: Requirements 2.9.4**

**Property 26: Device language detection**
*For any* device language setting on first launch, if the device language is supported (en or hi), the app should initialize with that language; otherwise, it should default to English.
**Validates: Requirements 2.9.3**

**Property 27: Notification navigation is type-specific**
*For any* notification with a type and associated data, tapping the notification should navigate to the screen corresponding to that notification type.
**Validates: Requirements 2.10.4**

**Property 28: Notification types are handled**
*For any* notification type (price_alert, buyer_interest, trust_milestone), the notification service should be able to display it with appropriate title and body.
**Validates: Requirements 2.10.3**


## Testing Strategy

### Dual Testing Approach

This project requires both unit testing and property-based testing for comprehensive coverage:

**Unit Tests**: Verify specific examples, edge cases, and error conditions
- Specific user scenarios (demo login, empty transaction list)
- Edge cases (empty strings, null values, boundary conditions)
- Error conditions (network failures, permission denials)
- Integration points between components
- Platform-specific behavior

**Property Tests**: Verify universal properties across all inputs
- Data transformations (compression, sorting, categorization)
- API contracts (request/response validation)
- State management (cache consistency, queue operations)
- Round-trip properties (serialization, upload/download)
- Invariants (distance calculations, tier thresholds)

Both approaches are complementary and necessary. Unit tests catch concrete bugs in specific scenarios, while property tests verify general correctness across the input space.

### Property-Based Testing Configuration

**Library Selection**: 
- JavaScript/TypeScript: fast-check (recommended for React Native)
- Alternative: jsverify

**Test Configuration**:
- Minimum 100 iterations per property test (due to randomization)
- Seed-based reproducibility for failed tests
- Shrinking enabled to find minimal failing examples
- Timeout: 30 seconds per property test

**Test Tagging**:
Each property-based test must include a comment tag referencing the design property:
```typescript
// Feature: mobile-app, Property 1: Audio recording produces valid files
```

**Property Test Implementation**:
- Each correctness property listed above must be implemented as a single property-based test
- Tests should use generators for random input creation
- Tests should validate the property assertion
- Failed tests should report the counterexample

### Test Organization

```
__tests__/
├── unit/
│   ├── components/
│   │   ├── Button.test.tsx
│   │   ├── Card.test.tsx
│   │   └── ProgressCircle.test.tsx
│   ├── services/
│   │   ├── api.test.ts
│   │   ├── cache.test.ts
│   │   ├── location.test.ts
│   │   └── permissions.test.ts
│   ├── store/
│   │   ├── authSlice.test.ts
│   │   ├── transactionsSlice.test.ts
│   │   └── pricesSlice.test.ts
│   └── utils/
│       ├── compression.test.ts
│       ├── validation.test.ts
│       └── formatting.test.ts
├── property/
│   ├── audio.property.test.ts
│   ├── permissions.property.test.ts
│   ├── s3Upload.property.test.ts
│   ├── transcription.property.test.ts
│   ├── transactions.property.test.ts
│   ├── prices.property.test.ts
│   ├── distance.property.test.ts
│   ├── cache.property.test.ts
│   ├── classification.property.test.ts
│   ├── listings.property.test.ts
│   ├── trustScore.property.test.ts
│   ├── offlineQueue.property.test.ts
│   ├── localization.property.test.ts
│   └── notifications.property.test.ts
├── integration/
│   ├── voiceTransaction.integration.test.tsx
│   ├── priceIntelligence.integration.test.tsx
│   ├── freshnessScanner.integration.test.tsx
│   ├── marketplace.integration.test.tsx
│   └── offlineSync.integration.test.tsx
└── e2e/
    ├── authentication.e2e.ts
    ├── voiceTransaction.e2e.ts
    ├── priceCheck.e2e.ts
    ├── scanner.e2e.ts
    └── marketplace.e2e.ts
```

### Test Coverage Goals

- Overall code coverage: > 80%
- Critical paths coverage: 100% (auth, transactions, offline sync)
- Property tests: All 28 properties implemented
- Unit tests: All services, utilities, and Redux slices
- Integration tests: All major user flows
- E2E tests: Critical user journeys on both platforms

### Testing Tools

- **Jest**: Unit and integration test runner
- **React Native Testing Library**: Component testing
- **fast-check**: Property-based testing
- **Detox**: E2E testing on real devices/emulators
- **Mock Service Worker**: API mocking
- **Redux Mock Store**: State management testing

### Mock Data Strategy

**Demo Mode**:
- Complete mock data for all API endpoints
- Stored in src/mocks/data.json
- Simulates realistic scenarios
- Includes edge cases (empty lists, errors)

**Test Mocks**:
- Mock AWS services (S3, API Gateway)
- Mock native modules (Camera, Voice, Geolocation)
- Mock AsyncStorage
- Mock network connectivity

### Continuous Testing

- Run unit tests on every commit
- Run property tests on every PR
- Run integration tests before release
- Run E2E tests on release candidates
- Monitor test execution time (< 5 minutes for unit/property tests)


## Platform-Specific Considerations

### Android-Specific Design

**Build Configuration**:
- minSdkVersion: 21 (Android 5.0)
- targetSdkVersion: 33 (Android 13)
- Multi-dex enabled for large app
- ProGuard rules for release builds

**Permissions**:
- Runtime permissions for API 23+
- Manifest permissions for API 21-22
- Permission rationale dialogs
- Settings deep linking for blocked permissions

**UI Patterns**:
- Material Design components
- Floating Action Button for primary actions
- Bottom navigation bar
- Swipe gestures for actions
- Ripple effects on touch

**Performance**:
- Hermes engine for faster startup
- Native driver for animations
- Optimized ProGuard rules
- APK size optimization

**Testing**:
- Test on Android 5.0, 8.0, 10.0, 13.0
- Test on devices: Samsung Galaxy J2 (2GB RAM), Pixel 4a, OnePlus Nord

### iOS-Specific Design

**Build Configuration**:
- Minimum deployment target: iOS 12.0
- Swift bridging for native modules
- CocoaPods for dependency management
- Code signing and provisioning

**Permissions**:
- Info.plist usage descriptions
- Permission request timing
- Settings deep linking
- Graceful degradation

**UI Patterns**:
- Human Interface Guidelines
- Tab bar navigation
- Swipe gestures
- Native animations
- Safe area handling

**Performance**:
- Optimize for older devices (iPhone 6s)
- Lazy loading for heavy screens
- Image caching
- IPA size optimization

**Testing**:
- Test on iOS 12.0, 14.0, 16.0
- Test on devices: iPhone 6s, iPhone SE (2020), iPhone 13

### Cross-Platform Considerations

**Shared Code**: 90%+
- All business logic
- Redux state management
- API integration
- Utility functions

**Platform-Specific Code**: < 10%
- Native module bridges
- Platform-specific UI components
- Permission handling differences
- Build configurations

**Conditional Rendering**:
```typescript
import { Platform } from 'react-native';

const styles = StyleSheet.create({
  button: {
    ...Platform.select({
      ios: { shadowOpacity: 0.3 },
      android: { elevation: 4 },
    }),
  },
});
```

## Security Design

### Authentication Security

**Credential Storage**:
- iOS: Keychain Services with kSecAttrAccessibleWhenUnlocked
- Android: EncryptedSharedPreferences with AES-256
- Never store passwords in plain text
- Clear credentials on logout

**Token Management**:
- JWT tokens with expiration
- Refresh token mechanism
- Automatic token refresh before expiry
- Secure token storage

**Demo Mode**:
- Clearly marked in UI
- No real data access
- Mock credentials only
- Cannot access production APIs

### Data Security

**In Transit**:
- HTTPS for all API calls
- Certificate pinning for API Gateway
- TLS 1.2+ required
- No sensitive data in URLs

**At Rest**:
- Encrypted AsyncStorage for sensitive data
- Secure file storage for audio/images
- No PII in logs
- Clear data on app uninstall

**Privacy**:
- Request permissions with clear rationale
- Minimal data collection
- No tracking without consent
- GDPR compliance considerations

### API Security

**Request Security**:
- Authentication token in headers
- Request signing for sensitive operations
- Rate limiting awareness
- Input validation before API calls

**Response Security**:
- Validate response structure
- Sanitize user-generated content
- Handle malicious responses gracefully
- No eval() or dynamic code execution

## Localization Design

### Translation Architecture

**i18next Configuration**:
- Language detection from device settings
- Fallback to English if language not supported
- Namespace organization by feature
- Lazy loading of translation files

**Translation Files**:
```
src/locales/
├── en/
│   ├── common.json
│   ├── home.json
│   ├── transactions.json
│   ├── prices.json
│   ├── scanner.json
│   ├── marketplace.json
│   ├── trustScore.json
│   └── settings.json
└── hi/
    ├── common.json
    ├── home.json
    ├── transactions.json
    ├── prices.json
    ├── scanner.json
    ├── marketplace.json
    ├── trustScore.json
    └── settings.json
```

**Translation Keys**:
- Dot notation: `home.welcomeMessage`
- Interpolation: `transactions.total: "Total: {{amount}}"`
- Pluralization: `items.count_one`, `items.count_other`
- Context: `button.submit_male`, `button.submit_female`

**Number and Date Formatting**:
- Currency: ₹ symbol for Indian Rupees
- Date format: DD/MM/YYYY for India
- Number format: Indian numbering system (lakhs, crores)
- Time format: 12-hour with AM/PM

### RTL Support

While Hindi is LTR, the architecture supports RTL for future languages:
- Flexbox with start/end instead of left/right
- I18nManager for RTL detection
- Mirrored icons for directional elements

## Accessibility Design

### Visual Accessibility

**High Contrast Mode**:
- Detect system high contrast setting
- Increase contrast ratios to WCAG AAA (7:1)
- Thicker borders and separators
- Stronger color differentiation

**Large Text Support**:
- Respect system text size settings
- Scale UI elements proportionally
- Minimum font size: 14pt
- Maximum scale: 200%

**Color Blindness**:
- Don't rely solely on color for information
- Use icons and labels with colors
- Test with color blindness simulators
- Patterns in addition to colors

### Touch Accessibility

**Touch Targets**:
- Minimum size: 44x44 points (iOS), 48x48dp (Android)
- Adequate spacing between targets (8pt minimum)
- Visual feedback on touch
- Haptic feedback for important actions

### Screen Reader Support

**iOS VoiceOver**:
- Accessibility labels for all interactive elements
- Accessibility hints for complex interactions
- Accessibility traits (button, header, link)
- Grouped elements for logical reading order

**Android TalkBack**:
- Content descriptions for all views
- Accessibility actions for custom gestures
- Focus order management
- Announcement for dynamic content

**Implementation**:
```typescript
<TouchableOpacity
  accessible={true}
  accessibilityLabel="Record voice transaction"
  accessibilityHint="Double tap to start recording"
  accessibilityRole="button"
>
  <MicrophoneIcon />
</TouchableOpacity>
```

## Analytics and Monitoring

### Event Tracking

**Screen Views**:
- Track all screen navigations
- Include screen name and timestamp
- Track time spent on each screen

**Feature Usage**:
- Voice transaction initiated/completed
- Price check performed
- Scanner used
- Listing created
- Trust score viewed

**User Actions**:
- Button clicks with button ID
- Form submissions
- Search queries
- Filter applications
- Swipe gestures

**System Events**:
- App launch
- App background/foreground
- Offline mode entered/exited
- Sync completed
- Errors occurred

### Performance Monitoring

**Metrics**:
- App launch time
- Screen transition time
- API response time
- Memory usage
- Battery consumption
- Network usage

**Crash Reporting**:
- Automatic crash detection
- Stack traces with source maps
- Device and OS information
- User actions before crash
- App state snapshot

**Custom Metrics**:
- Offline queue size
- Cache hit rate
- Sync success rate
- Permission grant rate
- Feature adoption rate

### Analytics Platform

**Firebase Analytics** (Recommended):
- Free tier sufficient
- Automatic screen tracking
- Custom event tracking
- User properties
- Audience segmentation
- Integration with Crashlytics

**Alternative: AWS Pinpoint**:
- Native AWS integration
- Custom event tracking
- User segmentation
- Campaign management
- Analytics dashboard

## Build and Deployment Design

### Environment Configuration

**Environment Variables**:
```
API_BASE_URL=https://api.example.com
AWS_REGION=ap-south-1
S3_BUCKET_NAME=vendor-app-uploads
FIREBASE_PROJECT_ID=vendor-app
SENTRY_DSN=https://...
```

**Environment Files**:
- .env.development
- .env.staging
- .env.production

**Configuration Loading**:
- react-native-config for environment variables
- Platform-specific configurations
- Build-time variable injection

### Android Build

**Debug Build**:
```bash
npx react-native run-android
```

**Release Build**:
```bash
cd android
./gradlew assembleRelease  # APK
./gradlew bundleRelease    # AAB for Play Store
```

**Signing Configuration**:
- Release keystore (not in version control)
- Signing config in gradle.properties
- ProGuard rules for minification
- Version code auto-increment

**APK Optimization**:
- Enable Hermes engine
- ProGuard minification
- Resource shrinking
- Split APKs by ABI (optional)

### iOS Build

**Debug Build**:
```bash
npx react-native run-ios
```

**Release Build**:
```bash
cd ios
xcodebuild archive -workspace VendorApp.xcworkspace -scheme VendorApp
xcodebuild -exportArchive -archivePath ... -exportPath ...
```

**Code Signing**:
- Development certificate for testing
- Distribution certificate for App Store
- Provisioning profiles
- Automatic signing in Xcode

**IPA Optimization**:
- Bitcode enabled
- App thinning
- On-demand resources
- Asset catalog optimization

### CI/CD Pipeline

**Automated Builds**:
- Build on every commit (debug)
- Build on PR merge (release)
- Automated testing before build
- Version bumping

**Distribution**:
- Internal testing: Firebase App Distribution
- Beta testing: TestFlight (iOS), Google Play Internal Testing (Android)
- Production: App Store, Google Play Store

## Deployment Strategy

### Phased Rollout

**Phase 1: Internal Testing** (Week 1)
- Deploy to development team
- Test all features
- Fix critical bugs
- Gather feedback

**Phase 2: Beta Testing** (Week 2-3)
- Deploy to 50-100 beta users
- Monitor crash reports
- Collect user feedback
- Iterate on UX issues

**Phase 3: Staged Rollout** (Week 4)
- Release to 10% of users
- Monitor metrics and crashes
- Increase to 50% if stable
- Full rollout if no issues

**Phase 4: Post-Launch** (Ongoing)
- Monitor analytics
- Address user feedback
- Release updates every 2 weeks
- Maintain backward compatibility

### Rollback Plan

- Keep previous version available
- Monitor crash rate (threshold: 1%)
- Automatic rollback if threshold exceeded
- Manual rollback option
- User notification for critical updates


## Implementation Notes

### Critical Implementation Details

**1. Offline Queue Persistence**
- Queue must survive app restarts
- Use AsyncStorage for queue persistence
- Serialize operations with JSON
- Handle queue corruption gracefully

**2. Cache TTL Management**
- Store timestamp with each cache entry
- Check expiration on retrieval
- Background cleanup of expired entries
- User-visible cache age indicators

**3. Image Compression**
- Use react-native-image-resizer
- Compress before upload, not after capture
- Maintain aspect ratio
- Progressive quality reduction if still too large

**4. Audio Recording**
- Request permission before showing recording UI
- Handle interruptions (phone calls, other apps)
- Clean up temporary files after upload
- Limit recording duration to prevent large files

**5. Location Services**
- Request permission with clear rationale
- Use cached location if recent (< 5 minutes)
- Timeout location requests (10 seconds)
- Fallback to manual location entry

**6. Push Notifications**
- Register device token on login
- Handle token refresh
- Unregister on logout
- Test on physical devices (not emulators)

**7. State Persistence**
- Persist Redux state on app background
- Hydrate state on app launch
- Handle migration for state schema changes
- Clear state on logout

**8. Navigation State**
- Persist navigation state for app restart
- Deep linking for notifications
- Handle back button (Android)
- Modal navigation for forms

### Development Workflow

**1. Setup**:
```bash
# Clone repo
git clone <repo-url>
cd mobile-app

# Install dependencies
npm install

# iOS setup
cd ios && pod install && cd ..

# Run on Android
npx react-native run-android

# Run on iOS
npx react-native run-ios
```

**2. Development**:
- Use TypeScript strict mode
- Follow ESLint rules
- Format with Prettier
- Write tests alongside code
- Use React DevTools for debugging

**3. Testing**:
```bash
# Unit and property tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage

# E2E tests
npm run test:e2e:android
npm run test:e2e:ios
```

**4. Building**:
```bash
# Android debug
npm run android

# Android release
npm run build:android

# iOS debug
npm run ios

# iOS release
npm run build:ios
```

### Code Organization

**Feature-Based Structure**:
```
src/
├── screens/
│   ├── Home/
│   │   ├── HomeScreen.tsx
│   │   ├── HomeScreen.styles.ts
│   │   └── components/
│   ├── VoiceTransaction/
│   ├── Prices/
│   ├── Scanner/
│   ├── Marketplace/
│   └── TrustScore/
├── components/
│   ├── common/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── Input.tsx
│   └── navigation/
├── services/
│   ├── api.ts
│   ├── s3.ts
│   ├── cache.ts
│   ├── offlineQueue.ts
│   ├── permissions.ts
│   ├── location.ts
│   └── notifications.ts
├── store/
│   ├── index.ts
│   ├── slices/
│   │   ├── authSlice.ts
│   │   ├── transactionsSlice.ts
│   │   ├── pricesSlice.ts
│   │   ├── marketplaceSlice.ts
│   │   ├── trustScoreSlice.ts
│   │   └── uiSlice.ts
│   └── middleware/
├── utils/
│   ├── compression.ts
│   ├── validation.ts
│   ├── formatting.ts
│   └── distance.ts
├── types/
│   ├── api.ts
│   ├── models.ts
│   └── navigation.ts
├── hooks/
│   ├── useOffline.ts
│   ├── usePermissions.ts
│   └── useLocation.ts
├── locales/
│   ├── en/
│   └── hi/
├── mocks/
│   └── data.json
└── config/
    ├── aws.ts
    ├── navigation.ts
    └── theme.ts
```

### Naming Conventions

**Files**: PascalCase for components, camelCase for utilities
- Components: `HomeScreen.tsx`, `Button.tsx`
- Services: `apiService.ts`, `cacheService.ts`
- Utilities: `compression.ts`, `validation.ts`

**Variables**: camelCase
- `vendorId`, `transactionList`, `isOffline`

**Constants**: UPPER_SNAKE_CASE
- `API_BASE_URL`, `MAX_RETRY_ATTEMPTS`, `CACHE_TTL`

**Types/Interfaces**: PascalCase
- `Transaction`, `PriceComparison`, `APIService`

**Redux Actions**: camelCase with feature prefix
- `auth/login`, `transactions/create`, `prices/fetch`

### Code Quality Standards

**TypeScript**:
- Strict mode enabled
- No implicit any
- Explicit return types for functions
- Interface over type for objects

**React**:
- Functional components only
- Hooks for state and effects
- Memoization for expensive computations
- Proper dependency arrays

**Testing**:
- Test file naming: `*.test.ts` or `*.test.tsx`
- Property tests: `*.property.test.ts`
- E2E tests: `*.e2e.ts`
- Minimum 80% coverage

**Documentation**:
- JSDoc comments for public APIs
- README for each major module
- Inline comments for complex logic
- Architecture decision records (ADRs)

## Risk Mitigation

### Technical Risks

**Risk 1: React Native version compatibility**
- Mitigation: Use stable LTS version (0.71+)
- Test on multiple RN versions
- Pin dependencies to specific versions
- Regular dependency updates

**Risk 2: Native module linking failures**
- Mitigation: Follow official documentation exactly
- Test on clean install
- Document manual linking steps
- Provide troubleshooting guide

**Risk 3: Performance on low-end devices**
- Mitigation: Test early on 2GB RAM devices
- Profile memory and CPU usage
- Optimize critical paths first
- Implement performance budgets

**Risk 4: AWS backend changes**
- Mitigation: Version API endpoints
- Implement backward compatibility
- Monitor API changes
- Coordinate with backend team

**Risk 5: Platform-specific bugs**
- Mitigation: Test on both platforms continuously
- Use platform-specific code sparingly
- Maintain platform parity
- Document known platform differences

### User Experience Risks

**Risk 1: Permission denial**
- Mitigation: Clear rationale messages
- Provide fallback options
- Guide users to settings
- Graceful degradation

**Risk 2: Poor network conditions**
- Mitigation: Offline-first architecture
- Optimistic UI updates
- Clear loading states
- Retry mechanisms

**Risk 3: Low device storage**
- Mitigation: Cache size limits
- User-initiated cache clear
- Warn before large downloads
- Compress all uploads

**Risk 4: Language barriers**
- Mitigation: Complete Hindi translation
- Visual icons for clarity
- Simple, clear language
- Voice input as alternative

### Business Risks

**Risk 1: App Store rejection**
- Mitigation: Follow guidelines strictly
- Prepare detailed review notes
- Test all features thoroughly
- Respond quickly to feedback

**Risk 2: Low adoption**
- Mitigation: Comprehensive onboarding
- Demo mode for exploration
- Clear value proposition
- User feedback integration

**Risk 3: High support burden**
- Mitigation: Comprehensive documentation
- In-app help and FAQs
- Clear error messages
- Analytics to identify pain points

## Future Enhancements

### Phase 2 Features

**WhatsApp Integration**:
- Send notifications via WhatsApp Business API
- Share listings on WhatsApp
- Transaction confirmations via WhatsApp

**Biometric Authentication**:
- Fingerprint login
- Face ID login
- Secure credential storage

**Advanced Analytics**:
- Sales trends dashboard
- Profit/loss tracking
- Inventory management
- Predictive analytics

### Phase 3 Features

**Voice Commands**:
- Voice navigation
- Voice search
- Voice form filling
- Multi-language voice support

**AR Features**:
- AR produce scanning
- AR marketplace preview
- AR measurement tools

**Blockchain Integration**:
- Blockchain-based trust score
- Immutable transaction records
- Smart contracts for marketplace

**Payment Integration**:
- UPI payment gateway
- Digital wallet integration
- Payment history
- Invoice generation

### Scalability Considerations

**Current Design Supports**:
- 10,000+ transactions per vendor
- 1,000+ marketplace listings
- 100+ concurrent users per device
- 100MB cache size

**Future Scaling Needs**:
- GraphQL for efficient data fetching
- Background sync optimization
- Incremental data loading
- Database migration to SQLite for complex queries

## Conclusion

This design provides a comprehensive blueprint for building native mobile applications that replicate the web frontend functionality while optimizing for mobile constraints. The offline-first architecture ensures reliability in poor network conditions, while the modular design enables maintainability and testability. The correctness properties provide a formal specification for automated testing, ensuring the app behaves correctly across all scenarios.

The design balances native mobile UX patterns with cross-platform code sharing, achieving 90%+ code reuse while maintaining platform-specific polish. Performance optimizations target low-end devices (2GB RAM), ensuring accessibility for the target user base of street vendors in India.


# Design Document: Smart Vendors

## Overview

Smart Vendors is a voice-first Decision Intelligence platform architected for resource-constrained environments. The system employs a hybrid edge-cloud architecture where critical voice processing and offline capabilities run on-device, while computationally intensive tasks (ML inference, fraud detection) execute on cloud infrastructure. The design prioritizes three core principles:

1. **Voice-First Interaction**: Zero-typing interface using Bhashini API for speech recognition and synthesis
2. **Offline Resilience**: Local-first data architecture with eventual consistency
3. **Intelligent Optimization**: ML-driven recommendations for inventory, pricing, and waste reduction

The system integrates multiple external data sources (Agmarknet for prices, IMD for weather, Google Distance Matrix for logistics) and employs computer vision (YOLOv8) for produce quality assessment. A consensus-based fraud detection system ensures marketplace integrity while a usage-based Trust Score enables financial inclusion.

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Mobile Client (React Native)             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Voice UI     │  │ Camera       │  │ Local DB     │      │
│  │ (Bhashini)   │  │ (CV Module)  │  │ (SQLite)     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTPS/WebSocket
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway (FastAPI)                    │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Voice        │   │ Price        │   │ ML           │
│ Processing   │   │ Intelligence │   │ Services     │
│ Service      │   │ Service      │   │ Service      │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              PostgreSQL + Redis Cache                        │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Agmarknet    │   │ IMD Weather  │   │ WhatsApp     │
│ API          │   │ API          │   │ Business API │
└──────────────┘   └──────────────┘   └──────────────┘
```

### Technology Stack

**Frontend**:
- React Native with offline-first architecture
- SQLite for local persistence
- React Native Voice for audio capture
- React Native Camera for image capture

**Backend**:
- FastAPI (Python 3.11+) for API services
- PostgreSQL 15 for relational data
- Redis for caching and real-time features
- Celery for async task processing

**ML/AI**:
- Bhashini API for speech-to-text and text-to-speech
- Gemini Flash for NLP and business logic
- YOLOv8 for produce classification
- Scikit-learn Random Forest for demand prediction
- Isolation Forest for anomaly detection

**External Integrations**:
- Agmarknet API for market prices
- OpenWeather/IMD for weather data
- WhatsApp Business API for notifications
- Google Distance Matrix for logistics


## Components and Interfaces

### 1. Voice Processing Service

**Responsibilities**:
- Convert speech to text using Bhashini API
- Extract structured transaction data from natural language
- Generate voice responses in vendor's preferred language
- Maintain conversation context across exchanges

**Key Interfaces**:

```python
class VoiceProcessor:
    def transcribe_audio(audio_bytes: bytes, language: str) -> TranscriptionResult:
        """
        Converts audio to text using Bhashini API.
        
        Args:
            audio_bytes: Raw audio data in WAV/MP3 format
            language: ISO language code (hi, en, bho)
            
        Returns:
            TranscriptionResult with text and confidence score
        """
        
    def extract_transaction(text: str, context: ConversationContext) -> Transaction:
        """
        Extracts structured transaction data from natural language.
        
        Args:
            text: Transcribed text from speech
            context: Previous conversation exchanges for context
            
        Returns:
            Transaction object or None if extraction fails
        """
        
    def synthesize_speech(text: str, language: str) -> bytes:
        """
        Converts text to speech using Bhashini API.
        
        Args:
            text: Text to convert to speech
            language: Target language for synthesis
            
        Returns:
            Audio bytes in MP3 format
        """
```

**Data Models**:

```python
@dataclass
class TranscriptionResult:
    text: str
    confidence: float  # 0.0 to 1.0
    language_detected: str
    timestamp: datetime

@dataclass
class Transaction:
    vendor_id: str
    item_name: str
    quantity: float
    unit: str  # kg, piece, dozen
    price: float
    timestamp: datetime
    
@dataclass
class ConversationContext:
    vendor_id: str
    recent_exchanges: List[str]  # Last 5 exchanges
    current_intent: str  # record_sale, query_price, etc.
```

### 2. Price Intelligence Service

**Responsibilities**:
- Fetch real-time prices from Agmarknet API
- Cache prices with TTL for offline access
- Validate vendor-reported prices using consensus algorithm
- Send price change alerts via WhatsApp

**Key Interfaces**:

```python
class PriceIntelligence:
    def get_current_prices(item: str, location: Location) -> List[PriceData]:
        """
        Retrieves current market prices for an item.
        
        Args:
            item: Produce item name (standardized)
            location: Vendor's location for proximity sorting
            
        Returns:
            List of PriceData from nearby mandis, sorted by distance
        """
        
    def validate_price(reported_price: PriceReport) -> ValidationResult:
        """
        Validates vendor-reported price using consensus algorithm.
        
        Args:
            reported_price: Price report from vendor
            
        Returns:
            ValidationResult with status and confidence score
        """
        
    def detect_price_anomaly(price_report: PriceReport) -> AnomalyScore:
        """
        Uses Isolation Forest to detect fraudulent price reports.
        
        Args:
            price_report: Price report to analyze
            
        Returns:
            AnomalyScore with fraud probability
        """
```

**Data Models**:

```python
@dataclass
class PriceData:
    item_name: str
    mandi_name: str
    price_per_kg: float
    distance_km: float
    timestamp: datetime
    source: str  # agmarknet, vendor_consensus
    
@dataclass
class PriceReport:
    vendor_id: str
    item_name: str
    price: float
    location: Location
    timestamp: datetime
    
@dataclass
class ValidationResult:
    is_valid: bool
    confidence: float
    peer_consensus_price: float
    deviation_percentage: float
    
@dataclass
class Location:
    latitude: float
    longitude: float
    district: str
```

### 3. Weather Optimization Service

**Responsibilities**:
- Fetch weather forecasts from IMD/OpenWeather
- Generate inventory recommendations based on weather predictions
- Calculate risk scores for different produce categories
- Provide voice-based explanations for recommendations

**Key Interfaces**:

```python
class WeatherOptimizer:
    def get_daily_recommendations(vendor_id: str) -> List[InventoryRecommendation]:
        """
        Generates morning inventory recommendations based on weather.
        
        Args:
            vendor_id: Unique vendor identifier
            
        Returns:
            List of recommendations for different produce categories
        """
        
    def calculate_weather_risk(forecast: WeatherForecast, item_category: str) -> RiskScore:
        """
        Calculates weather-related risk for produce category.
        
        Args:
            forecast: Weather forecast for the day
            item_category: Produce category (leafy, root, fruit)
            
        Returns:
            RiskScore with risk level and mitigation suggestions
        """
```

**Data Models**:

```python
@dataclass
class WeatherForecast:
    date: date
    max_temp_celsius: float
    min_temp_celsius: float
    rain_probability: float  # 0.0 to 1.0
    humidity: float
    location: Location
    
@dataclass
class InventoryRecommendation:
    item_category: str
    action: str  # reduce, maintain, increase
    percentage_change: float  # -30 to +30
    reasoning: str  # Voice-friendly explanation
    confidence: float
    
@dataclass
class RiskScore:
    risk_level: str  # low, medium, high
    score: float  # 0.0 to 1.0
    factors: List[str]  # Contributing risk factors
```

### 4. Freshness Scanner Service

**Responsibilities**:
- Classify produce freshness using YOLOv8 computer vision model
- Estimate remaining shelf life
- Suggest alternative uses for B-Grade produce
- Provide confidence scores for classifications

**Key Interfaces**:

```python
class FreshnessScanner:
    def classify_produce(image_bytes: bytes) -> FreshnessClassification:
        """
        Classifies produce freshness from image.
        
        Args:
            image_bytes: JPEG/PNG image data
            
        Returns:
            FreshnessClassification with category and confidence
        """
        
    def estimate_shelf_life(classification: FreshnessClassification, item: str) -> ShelfLifeEstimate:
        """
        Estimates remaining shelf life based on visual assessment.
        
        Args:
            classification: Freshness classification result
            item: Produce item name
            
        Returns:
            ShelfLifeEstimate with hours remaining
        """
```

**Data Models**:

```python
@dataclass
class FreshnessClassification:
    category: str  # Fresh, B-Grade, Waste
    confidence: float
    visual_indicators: List[str]  # spots, wilting, discoloration
    item_detected: str
    timestamp: datetime
    
@dataclass
class ShelfLifeEstimate:
    hours_remaining: int
    confidence: float
    storage_recommendations: List[str]
```

### 5. Waste Monetization Service

**Responsibilities**:
- Calculate residual value of B-Grade produce
- List items on B-Grade Marketplace
- Match vendors with buyers (juice stalls, pickle makers)
- Manage Mandi Credits system

**Key Interfaces**:

```python
class WasteMonetization:
    def calculate_residual_value(item: str, weight_kg: float, condition: str) -> ResidualValue:
        """
        Calculates recoverable value from B-Grade produce.
        Formula: V_residual = (W × C_rate) - L_fee
        
        Args:
            item: Produce item name
            weight_kg: Weight in kilograms
            condition: B-Grade or Waste
            
        Returns:
            ResidualValue with price and breakdown
        """
        
    def list_on_marketplace(listing: MarketplaceListing) -> ListingResult:
        """
        Lists B-Grade produce on marketplace and notifies buyers.
        
        Args:
            listing: Marketplace listing details
            
        Returns:
            ListingResult with listing ID and notification status
        """
        
    def find_nearby_buyers(item: str, location: Location, radius_km: float) -> List[Buyer]:
        """
        Finds potential buyers within specified radius.
        
        Args:
            item: Produce item name
            location: Vendor location
            radius_km: Search radius
            
        Returns:
            List of Buyer profiles sorted by distance
        """
```

**Data Models**:

```python
@dataclass
class ResidualValue:
    base_value: float  # W × C_rate
    logistics_fee: float  # L_fee
    net_value: float  # base_value - logistics_fee
    mandi_credits: int
    
@dataclass
class MarketplaceListing:
    vendor_id: str
    item_name: str
    weight_kg: float
    condition: str
    price: float
    location: Location
    available_until: datetime
    
@dataclass
class Buyer:
    buyer_id: str
    business_type: str  # juice_stall, pickle_maker, compost
    distance_km: float
    rating: float
    preferred_items: List[str]
```

### 6. Trust Score Engine

**Responsibilities**:
- Calculate vendor Trust Score based on app usage
- Track scoring factors (consistency, volume, waste reduction)
- Generate PM-SVANidhi eligibility reports
- Manage tier progression (Bronze, Silver, Gold)

**Key Interfaces**:

```python
class TrustScoreEngine:
    def calculate_trust_score(vendor_id: str) -> TrustScore:
        """
        Calculates comprehensive Trust Score for vendor.
        
        Args:
            vendor_id: Unique vendor identifier
            
        Returns:
            TrustScore with current score and tier
        """
        
    def generate_loan_eligibility_report(vendor_id: str) -> LoanEligibilityReport:
        """
        Generates PM-SVANidhi loan eligibility report.
        
        Args:
            vendor_id: Unique vendor identifier
            
        Returns:
            LoanEligibilityReport with score and recommendations
        """
        
    def update_score_factors(vendor_id: str, activity: Activity) -> ScoreUpdate:
        """
        Updates Trust Score based on vendor activity.
        
        Args:
            vendor_id: Unique vendor identifier
            activity: Recent activity (transaction, marketplace, etc.)
            
        Returns:
            ScoreUpdate with new score and change explanation
        """
```

**Data Models**:

```python
@dataclass
class TrustScore:
    vendor_id: str
    current_score: int
    tier: str  # Bronze (100+), Silver (250+), Gold (500+)
    factors: Dict[str, float]  # consistency, volume, waste_reduction
    last_updated: datetime
    
@dataclass
class LoanEligibilityReport:
    vendor_id: str
    trust_score: int
    eligible: bool
    recommended_loan_amount: float
    digital_ledger_months: int
    verification_certificate: str  # Digital signature
    
@dataclass
class Activity:
    activity_type: str  # transaction, marketplace_sale, etc.
    timestamp: datetime
    value: float
```

### 7. Fraud Detection Service

**Responsibilities**:
- Implement consensus algorithm for price validation
- Use Isolation Forest ML for anomaly detection
- Cross-reference with Agmarknet official rates
- Manage vendor reputation and suspension

**Key Interfaces**:

```python
class FraudDetection:
    def validate_with_consensus(price_report: PriceReport) -> ConsensusResult:
        """
        Validates price using peer consensus algorithm.
        
        Args:
            price_report: Price report to validate
            
        Returns:
            ConsensusResult with validation status and peer data
        """
        
    def detect_anomaly_ml(price_report: PriceReport, vendor_history: List[PriceReport]) -> AnomalyDetection:
        """
        Uses Isolation Forest to detect price anomalies.
        
        Args:
            price_report: Current price report
            vendor_history: Historical reports from vendor
            
        Returns:
            AnomalyDetection with fraud probability
        """
        
    def cross_reference_official(price_report: PriceReport) -> OfficialComparison:
        """
        Compares vendor price with Agmarknet official rates.
        
        Args:
            price_report: Price report to verify
            
        Returns:
            OfficialComparison with deviation analysis
        """
```

**Data Models**:

```python
@dataclass
class ConsensusResult:
    is_consensus: bool
    peer_reports: List[PriceReport]  # Reports from nearby vendors
    consensus_price: float
    deviation: float
    confidence: float
    
@dataclass
class AnomalyDetection:
    is_anomaly: bool
    fraud_probability: float  # 0.0 to 1.0
    anomaly_score: float  # Isolation Forest score
    contributing_factors: List[str]
    
@dataclass
class OfficialComparison:
    official_price: float
    reported_price: float
    deviation_percentage: float
    within_acceptable_range: bool
```


## Data Models

### Core Entities

**Vendor**:
```python
@dataclass
class Vendor:
    vendor_id: str  # UUID
    phone_number: str  # Primary identifier
    name: str
    preferred_language: str  # hi, en, bho
    location: Location
    registration_date: datetime
    trust_score: int
    tier: str  # Bronze, Silver, Gold
    is_active: bool
```

**Transaction**:
```python
@dataclass
class Transaction:
    transaction_id: str  # UUID
    vendor_id: str
    item_name: str
    quantity: float
    unit: str
    price_per_unit: float
    total_amount: float
    timestamp: datetime
    recorded_via: str  # voice, manual, offline_sync
    sync_status: str  # synced, pending, conflict
```

**Inventory**:
```python
@dataclass
class Inventory:
    inventory_id: str
    vendor_id: str
    item_name: str
    quantity_kg: float
    purchase_price: float
    freshness_status: str  # Fresh, B-Grade, Waste
    last_assessed: datetime
    estimated_shelf_life_hours: int
```

**MarketPrice**:
```python
@dataclass
class MarketPrice:
    price_id: str
    item_name: str
    mandi_name: str
    price_per_kg: float
    location: Location
    timestamp: datetime
    source: str  # agmarknet, vendor_consensus
    confidence: float
```

### Database Schema

**PostgreSQL Tables**:

```sql
-- Vendors table
CREATE TABLE vendors (
    vendor_id UUID PRIMARY KEY,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    name VARCHAR(100),
    preferred_language VARCHAR(5),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    district VARCHAR(50),
    registration_date TIMESTAMP,
    trust_score INTEGER DEFAULT 0,
    tier VARCHAR(20) DEFAULT 'Bronze',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Transactions table
CREATE TABLE transactions (
    transaction_id UUID PRIMARY KEY,
    vendor_id UUID REFERENCES vendors(vendor_id),
    item_name VARCHAR(100),
    quantity DECIMAL(10, 2),
    unit VARCHAR(20),
    price_per_unit DECIMAL(10, 2),
    total_amount DECIMAL(10, 2),
    timestamp TIMESTAMP,
    recorded_via VARCHAR(20),
    sync_status VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Market prices table
CREATE TABLE market_prices (
    price_id UUID PRIMARY KEY,
    item_name VARCHAR(100),
    mandi_name VARCHAR(100),
    price_per_kg DECIMAL(10, 2),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    timestamp TIMESTAMP,
    source VARCHAR(50),
    confidence DECIMAL(3, 2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Inventory table
CREATE TABLE inventory (
    inventory_id UUID PRIMARY KEY,
    vendor_id UUID REFERENCES vendors(vendor_id),
    item_name VARCHAR(100),
    quantity_kg DECIMAL(10, 2),
    purchase_price DECIMAL(10, 2),
    freshness_status VARCHAR(20),
    last_assessed TIMESTAMP,
    estimated_shelf_life_hours INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Marketplace listings table
CREATE TABLE marketplace_listings (
    listing_id UUID PRIMARY KEY,
    vendor_id UUID REFERENCES vendors(vendor_id),
    item_name VARCHAR(100),
    weight_kg DECIMAL(10, 2),
    condition VARCHAR(20),
    price DECIMAL(10, 2),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    available_until TIMESTAMP,
    status VARCHAR(20),  -- active, sold, expired
    created_at TIMESTAMP DEFAULT NOW()
);

-- Trust score history table
CREATE TABLE trust_score_history (
    history_id UUID PRIMARY KEY,
    vendor_id UUID REFERENCES vendors(vendor_id),
    score_change INTEGER,
    activity_type VARCHAR(50),
    timestamp TIMESTAMP,
    new_score INTEGER
);

-- Price reports table (for consensus validation)
CREATE TABLE price_reports (
    report_id UUID PRIMARY KEY,
    vendor_id UUID REFERENCES vendors(vendor_id),
    item_name VARCHAR(100),
    price DECIMAL(10, 2),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    timestamp TIMESTAMP,
    validation_status VARCHAR(20),  -- pending, validated, flagged
    fraud_score DECIMAL(3, 2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_transactions_vendor ON transactions(vendor_id, timestamp DESC);
CREATE INDEX idx_market_prices_item ON market_prices(item_name, timestamp DESC);
CREATE INDEX idx_inventory_vendor ON inventory(vendor_id, freshness_status);
CREATE INDEX idx_price_reports_location ON price_reports(latitude, longitude, timestamp);
```

### Redis Cache Structure

```python
# Price cache (TTL: 1 hour)
KEY: "price:{item_name}:{district}"
VALUE: JSON serialized List[PriceData]

# Vendor session cache (TTL: 24 hours)
KEY: "session:{vendor_id}"
VALUE: JSON serialized ConversationContext

# Consensus cache (TTL: 30 minutes)
KEY: "consensus:{item_name}:{lat}:{lon}"
VALUE: JSON serialized ConsensusResult

# Weather forecast cache (TTL: 6 hours)
KEY: "weather:{district}:{date}"
VALUE: JSON serialized WeatherForecast
```


## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Voice Processing Properties

**Property 1: Speech transcription produces text output**
*For any* valid audio input in supported languages (Hindi, Hinglish, Bhojpuri), the Voice_Ledger should produce a transcription result with text and confidence score.
**Validates: Requirements 1.1**

**Property 2: Transaction extraction from natural language**
*For any* valid transaction utterance (containing item, quantity, and price), the Voice_Ledger should extract structured transaction data with all required fields populated.
**Validates: Requirements 1.2**

**Property 3: Transaction storage round-trip**
*For any* extracted transaction, storing it to the database and then retrieving it should produce an equivalent transaction object with matching fields.
**Validates: Requirements 1.3**

**Property 4: Low-confidence transcription triggers clarification**
*For any* transcription with confidence below 60%, the Voice_Ledger should request clarification rather than proceeding with uncertain data.
**Validates: Requirements 1.4, 9.4**

**Property 5: Offline transaction eventual consistency**
*For any* transaction recorded in offline mode, when connectivity is restored, the transaction should eventually appear in the server database with matching data.
**Validates: Requirements 1.5, 8.3**

**Property 6: Daily summary completeness**
*For any* vendor's daily transactions, the generated summary should include total sales amount, list of items sold with quantities, and remaining inventory for each item.
**Validates: Requirements 1.6**

### Price Intelligence Properties

**Property 7: Price change alerts trigger on threshold**
*For any* item in vendor inventory, when market price changes by more than 10%, an alert should be generated and sent to the vendor.
**Validates: Requirements 2.2**

**Property 8: Price results include minimum mandi count**
*For any* price query, the results should include prices from at least 3 mandis (or all available if fewer than 3 exist) with distance indicators for each.
**Validates: Requirements 2.3**

**Property 9: Cached prices include staleness indicators**
*For any* price query when Agmarknet API is unavailable, the returned cached prices should include timestamps showing data age.
**Validates: Requirements 2.4, 8.4**

**Property 10: Price results sorted by geographic proximity**
*For any* price query from a specific location, the returned results should be ordered by distance from nearest to farthest mandi.
**Validates: Requirements 2.5**

**Property 11: Consensus validation uses peer data**
*For any* vendor price report, the consensus validation should compare against at least 3 nearby vendor reports within 2km radius (or all available if fewer than 3).
**Validates: Requirements 2.6, 7.1**

### Weather Optimization Properties

**Property 12: Weather-based recommendations within expected ranges**
*For any* weather forecast, the generated inventory recommendations should fall within expected ranges: 15-25% reduction for heat >42°C, 20-30% reduction for rain >70% probability, or standard/increased for optimal conditions.
**Validates: Requirements 3.2, 3.3, 3.4**

**Property 13: Recommendations incorporate vendor history**
*For any* two vendors with different historical sales patterns, given identical weather forecasts, the recommendations should differ based on their individual patterns and current inventory.
**Validates: Requirements 3.5**

**Property 14: Recommendation explanations match vendor language**
*For any* recommendation explanation request, the response should be in the vendor's preferred language as specified in their profile.
**Validates: Requirements 3.6**

### Freshness Assessment Properties

**Property 15: Produce classification into valid categories**
*For any* produce image, the Freshness_Scanner should classify it into exactly one of three categories: Fresh, B-Grade, or Waste.
**Validates: Requirements 4.1**

**Property 16: Classification results include category-specific information**
*For any* produce classification, Fresh results should include shelf life estimation, B-Grade results should include alternative use suggestions, and Waste results should include composting recommendations.
**Validates: Requirements 4.2, 4.3, 4.4**

**Property 17: Low-quality images trigger re-capture request**
*For any* image with insufficient quality for classification, the Freshness_Scanner should request a clearer photo rather than providing unreliable classification.
**Validates: Requirements 4.5**

**Property 18: Low-confidence classifications include confidence scores**
*For any* classification with confidence below 70%, the result should include the confidence score and request manual verification.
**Validates: Requirements 4.6**

### Waste Monetization Properties

**Property 19: Residual value calculation formula correctness**
*For any* B-Grade produce listing with weight W, category rate C_rate, and logistics fee L_fee, the calculated residual value should equal (W × C_rate) - L_fee.
**Validates: Requirements 5.1**

**Property 20: Marketplace notifications to nearby buyers**
*For any* B-Grade produce listing, notifications should be sent only to buyers within 5km radius who accept that produce type.
**Validates: Requirements 5.2**

**Property 21: Buyer-seller connection includes required information**
*For any* buyer interest expression, the facilitated WhatsApp connection should include pickup location, time window, and produce details.
**Validates: Requirements 5.3**

**Property 22: Transaction completion credits vendor account**
*For any* completed marketplace transaction, the vendor's Mandi_Credits balance should increase by the transaction's credit value.
**Validates: Requirements 5.4**

**Property 23: No-buyer fallback provides composting options**
*For any* listing with no buyer interest after 2 hours, the system should suggest composting facilities with pickup logistics information.
**Validates: Requirements 5.5**

**Property 24: Mandi Credits display includes conversion information**
*For any* Mandi_Credits balance query, the display should include current conversion rate to rupees and available redemption options.
**Validates: Requirements 5.6**

### Trust Score Properties

**Property 25: Consistent activity increases Trust Score**
*For any* vendor recording transactions consistently over time, their Trust_Score should increase (monotonically non-decreasing with activity).
**Validates: Requirements 6.1**

**Property 26: Trust Score thresholds trigger tier changes**
*For any* vendor whose Trust_Score crosses a threshold (100 for Bronze, 250 for Silver, 500 for Gold), their tier should update to the corresponding level.
**Validates: Requirements 6.2**

**Property 27: Loan eligibility report completeness**
*For any* loan eligibility request, the generated report should include Trust_Score, eligibility status, recommended loan amount, and digital ledger duration.
**Validates: Requirements 6.3**

**Property 28: Trust Score incorporates multiple factors**
*For any* two vendors with identical transaction volumes but different waste reduction or marketplace participation, their Trust_Scores should differ reflecting the additional factors.
**Validates: Requirements 6.4**

**Property 29: Trust Score certificate verifiability**
*For any* generated Trust_Score certificate, it should include a digital signature that can be cryptographically verified by third parties.
**Validates: Requirements 6.5**

**Property 30: Inactivity triggers engagement reminders**
*For any* vendor whose Trust_Score decreases due to inactivity, a reminder notification should be sent to encourage re-engagement.
**Validates: Requirements 6.6**

### Fraud Detection Properties

**Property 31: Price deviation flagging threshold**
*For any* vendor price report that deviates by more than 25% from peer consensus, the report should be flagged for review.
**Validates: Requirements 7.2**

**Property 32: Anomaly classification into valid categories**
*For any* detected price anomaly, the Isolation Forest model should classify it as either "genuine outlier" or "fraud" with confidence score.
**Validates: Requirements 7.3**

**Property 33: High-confidence fraud triggers exclusion**
*For any* price report classified as fraud with confidence >80%, the price should be excluded from public display and the vendor should receive a notification.
**Validates: Requirements 7.4**

**Property 34: Fraud flag accumulation triggers suspension**
*For any* vendor accumulating 3 or more fraud flags, their price reporting privileges should be temporarily suspended.
**Validates: Requirements 7.5**

**Property 35: Official rate cross-referencing when available**
*For any* price report when Agmarknet API is available, the consensus validation should include comparison with official rates as additional validation.
**Validates: Requirements 7.6**

### Offline Mode Properties

**Property 36: Connectivity loss triggers offline mode**
*For any* network connectivity loss, the system should switch to offline mode and display a visual indicator to the vendor.
**Validates: Requirements 8.1**

**Property 37: Offline transactions stored locally**
*For any* transaction recorded while in offline mode, the transaction should be stored in local device storage.
**Validates: Requirements 8.2**

**Property 38: Sync conflict resolution uses timestamps**
*For any* sync conflict where the same transaction exists offline and online, the system should resolve using timestamp-based logic (most recent wins) and notify the vendor.
**Validates: Requirements 8.6**

**Property 39: Critical actions queued in offline mode**
*For any* action requiring connectivity (price updates, marketplace listings) attempted in offline mode, the action should be queued and the vendor notified when sync completes.
**Validates: Requirements 8.5**

### Multilingual Properties

**Property 40: Language detection or selection on first launch**
*For any* vendor's first app launch, the system should either detect language from voice sample or prompt for manual selection, resulting in a stored language preference.
**Validates: Requirements 9.1**

**Property 41: Conversation context preservation**
*For any* multi-exchange conversation, the system should maintain context such that references to previous exchanges are correctly understood.
**Validates: Requirements 9.2**

**Property 42: Business terminology preservation**
*For any* translation between languages, specific business terms (mandi, kilo, bhav, etc.) should remain untranslated in the output.
**Validates: Requirements 9.3**

### WhatsApp Integration Properties

**Property 43: Registration creates WhatsApp linkage**
*For any* vendor registration with phone number, the system should create an association between the vendor account and WhatsApp number for notifications.
**Validates: Requirements 10.1**

**Property 44: Alerts delivered via WhatsApp**
*For any* generated price alert or weather warning, a message should be sent via WhatsApp Business API to the vendor's registered number.
**Validates: Requirements 10.2**

**Property 45: WhatsApp queries receive responses**
*For any* vendor query sent via WhatsApp message, the system should process it and send a response message.
**Validates: Requirements 10.3**

**Property 46: Marketplace communication includes privacy protection**
*For any* marketplace transaction communication, buyer and seller should be connected via WhatsApp without exposing personal phone numbers until both parties consent.
**Validates: Requirements 10.4**

**Property 47: Notification preferences respected**
*For any* vendor who has opted out of specific notification types, those notifications should not be sent, while critical alerts should still be delivered.
**Validates: Requirements 10.5**

**Property 48: WhatsApp failure triggers SMS fallback**
*For any* critical notification when WhatsApp Business API is unavailable, the system should send the notification via SMS instead.
**Validates: Requirements 10.6**

### Demand Prediction Properties

**Property 49: High demand predictions suggest price increases**
*For any* item with predicted high demand, the system should suggest price increases in the range of 5-15% with confidence scores.
**Validates: Requirements 11.2**

**Property 50: Low demand predictions suggest alternatives**
*For any* item with predicted low demand, the system should recommend either promotional pricing or alternative sales channels.
**Validates: Requirements 11.3**

**Property 51: Predictions incorporate multiple factors**
*For any* two identical items on different days, if factors differ (day of week, weather, festivals, demographics), the demand predictions should differ accordingly.
**Validates: Requirements 11.4**

**Property 52: Recommendations adapt to vendor behavior**
*For any* vendor who consistently ignores recommendations, subsequent recommendations should adapt based on the vendor's actual pricing behavior patterns.
**Validates: Requirements 11.6**

### Security and Privacy Properties

**Property 53: Data encryption on registration**
*For any* vendor registration, all personal and transaction data should be encrypted using AES-256 before storage.
**Validates: Requirements 12.1**

**Property 54: Vendor anonymization in aggregates**
*For any* aggregate analytics or marketplace listing, vendor identities should be anonymized such that personal identifiers cannot be recovered.
**Validates: Requirements 12.2**

**Property 55: Third-party sharing requires consent**
*For any* attempt to share vendor data with third parties (banks, government), the operation should fail unless explicit vendor consent has been recorded.
**Validates: Requirements 12.3**

**Property 56: Data deletion preserves anonymized analytics**
*For any* vendor data deletion request, all personal information should be removed while anonymized aggregate analytics should remain intact.
**Validates: Requirements 12.4**

**Property 57: OTP-based authentication**
*For any* authentication attempt, the system should use OTP verification sent via SMS or WhatsApp rather than password-based authentication.
**Validates: Requirements 12.5**

**Property 58: Suspicious access triggers lockout**
*For any* detected suspicious access pattern, the affected account should be locked and the vendor should receive an immediate notification.
**Validates: Requirements 12.6**


## Error Handling

### Voice Processing Errors

**Low Confidence Transcription**:
- Threshold: Confidence < 60%
- Action: Request repetition with voice guidance
- Fallback: After 3 failed attempts, offer manual text input option

**Unsupported Language Detection**:
- Detection: Language not in [Hindi, Hinglish, Bhojpuri, English]
- Action: Notify vendor and request language selection
- Fallback: Default to Hindi with option to change

**Transaction Extraction Failure**:
- Detection: Unable to extract required fields (item, quantity, price)
- Action: Ask clarifying questions via voice ("Which item?", "How much quantity?")
- Fallback: Provide voice menu with common items

**Audio Quality Issues**:
- Detection: High background noise, clipping, or distortion
- Action: Request re-recording with guidance on optimal conditions
- Fallback: Offer text input or structured form

### Price Intelligence Errors

**Agmarknet API Unavailable**:
- Detection: API timeout or error response
- Action: Serve cached prices with staleness indicator
- Fallback: Use vendor consensus prices if cache is stale (>24 hours)

**Insufficient Peer Data for Consensus**:
- Detection: Fewer than 3 nearby vendors reporting prices
- Action: Expand search radius to 5km
- Fallback: Display official Agmarknet price with "limited peer data" warning

**Price Validation Failure**:
- Detection: Price deviates >25% from consensus
- Action: Flag for review, request vendor confirmation
- Fallback: Display price with "unverified" tag, exclude from consensus

**Location Services Unavailable**:
- Detection: GPS disabled or permission denied
- Action: Request manual district selection
- Fallback: Use last known location with staleness indicator

### Weather Optimization Errors

**Weather API Failure**:
- Detection: IMD/OpenWeather API timeout or error
- Action: Use cached forecast from previous day
- Fallback: Provide generic seasonal recommendations

**Historical Data Insufficient**:
- Detection: Vendor has <7 days of transaction history
- Action: Use neighborhood aggregate patterns
- Fallback: Provide conservative recommendations (reduce by 10%)

**Extreme Weather Conditions**:
- Detection: Temperature >48°C or <5°C, rain >90% probability
- Action: Send urgent alert, recommend minimal purchasing
- Fallback: Suggest alternative income sources (prepared foods, non-perishables)

### Computer Vision Errors

**Image Classification Failure**:
- Detection: Model confidence <50% or no produce detected
- Action: Request clearer photo with guidance (lighting, distance, angle)
- Fallback: After 3 attempts, offer manual category selection

**Multiple Items in Image**:
- Detection: Model detects >1 produce type
- Action: Request single-item photo or ask vendor to specify which item
- Fallback: Classify each detected item separately

**Unsupported Produce Type**:
- Detection: Item not in trained model categories
- Action: Log for future model training, request manual classification
- Fallback: Use generic freshness indicators (color, texture)

### Marketplace Errors

**No Buyers Available**:
- Detection: No buyers within 5km radius or no responses after 2 hours
- Action: Suggest composting facilities with logistics
- Fallback: Offer to expand radius to 10km or reduce price

**Buyer-Seller Connection Failure**:
- Detection: WhatsApp message delivery failure
- Action: Retry via SMS
- Fallback: Provide phone numbers for direct contact

**Transaction Completion Dispute**:
- Detection: Buyer or seller reports transaction not completed
- Action: Request evidence (photos, timestamps), hold Mandi_Credits
- Fallback: Manual review by support team, refund if fraud detected

### Offline Mode Errors

**Local Storage Full**:
- Detection: Device storage <50MB available
- Action: Notify vendor, suggest deleting old data
- Fallback: Keep only last 24 hours of transactions, sync older data first

**Sync Conflict**:
- Detection: Same transaction ID exists with different data
- Action: Use timestamp-based resolution (most recent wins)
- Fallback: Create duplicate entry with conflict flag for manual review

**Partial Sync Failure**:
- Detection: Some transactions synced, others failed
- Action: Retry failed transactions with exponential backoff
- Fallback: Queue for next sync attempt, notify vendor of pending items

### Authentication and Security Errors

**OTP Delivery Failure**:
- Detection: SMS/WhatsApp delivery timeout
- Action: Retry via alternate channel (SMS if WhatsApp failed)
- Fallback: After 3 attempts, offer email OTP or support contact

**Suspicious Access Detected**:
- Detection: Login from new device, unusual location, or rapid failed attempts
- Action: Lock account, send notification to registered phone
- Fallback: Require additional verification (security questions, support call)

**Data Encryption Failure**:
- Detection: Encryption operation error
- Action: Reject data storage, log error, notify admin
- Fallback: No fallback - fail securely, do not store unencrypted data

**Consent Verification Failure**:
- Detection: Attempt to share data without recorded consent
- Action: Block operation, request explicit consent
- Fallback: No fallback - privacy violation prevention is critical

### General Error Handling Principles

1. **Graceful Degradation**: System should remain functional even when components fail
2. **User Communication**: Always inform vendor of errors in their preferred language
3. **Automatic Recovery**: Retry transient failures with exponential backoff
4. **Fail Securely**: Security and privacy errors should fail closed (deny operation)
5. **Error Logging**: All errors logged with context for debugging and improvement
6. **Offline Resilience**: Critical features (transaction recording) work offline
7. **User Guidance**: Provide actionable steps for vendor to resolve errors


## Testing Strategy

### Dual Testing Approach

Smart Vendors requires both unit testing and property-based testing to ensure comprehensive correctness:

**Unit Tests**: Verify specific examples, edge cases, and error conditions
- Specific transaction examples (edge cases like zero quantity, negative prices)
- Integration points between services (Voice → Database, Price → WhatsApp)
- Error handling scenarios (API failures, network timeouts)
- Authentication flows (OTP generation, verification)

**Property-Based Tests**: Verify universal properties across all inputs
- Transaction round-trip consistency across all valid inputs
- Price validation logic for any price report
- Weather recommendation ranges for any forecast
- Fraud detection for any price deviation pattern

Both approaches are complementary and necessary. Unit tests catch concrete bugs in specific scenarios, while property tests verify general correctness across the input space.

### Property-Based Testing Configuration

**Framework Selection**:
- **Python Backend**: Use Hypothesis library for property-based testing
- **React Native Frontend**: Use fast-check library for JavaScript/TypeScript
- **Integration Tests**: Use Hypothesis for end-to-end property testing

**Test Configuration**:
- Minimum 100 iterations per property test (due to randomization)
- Seed-based reproducibility for failed test cases
- Shrinking enabled to find minimal failing examples
- Timeout: 30 seconds per property test

**Property Test Tagging**:
Each property-based test must include a comment tag referencing the design document:

```python
# Feature: smart-mandi, Property 3: Transaction storage round-trip
@given(transactions=transaction_strategy())
def test_transaction_round_trip(transaction):
    stored_id = store_transaction(transaction)
    retrieved = get_transaction(stored_id)
    assert retrieved == transaction
```

**Generator Strategies**:

```python
# Transaction generator
@composite
def transaction_strategy(draw):
    return Transaction(
        vendor_id=draw(st.uuids()),
        item_name=draw(st.sampled_from(PRODUCE_ITEMS)),
        quantity=draw(st.floats(min_value=0.1, max_value=100.0)),
        unit=draw(st.sampled_from(['kg', 'piece', 'dozen'])),
        price=draw(st.floats(min_value=1.0, max_value=10000.0)),
        timestamp=draw(st.datetimes())
    )

# Price report generator
@composite
def price_report_strategy(draw):
    return PriceReport(
        vendor_id=draw(st.uuids()),
        item_name=draw(st.sampled_from(PRODUCE_ITEMS)),
        price=draw(st.floats(min_value=1.0, max_value=500.0)),
        location=draw(location_strategy()),
        timestamp=draw(st.datetimes())
    )

# Weather forecast generator
@composite
def weather_forecast_strategy(draw):
    return WeatherForecast(
        date=draw(st.dates()),
        max_temp_celsius=draw(st.floats(min_value=15.0, max_value=50.0)),
        min_temp_celsius=draw(st.floats(min_value=5.0, max_value=35.0)),
        rain_probability=draw(st.floats(min_value=0.0, max_value=1.0)),
        humidity=draw(st.floats(min_value=0.0, max_value=100.0)),
        location=draw(location_strategy())
    )
```

### Unit Testing Strategy

**Coverage Targets**:
- Core business logic: 90% code coverage
- API endpoints: 85% code coverage
- Error handling paths: 80% code coverage
- UI components: 70% code coverage

**Test Organization**:
```
tests/
├── unit/
│   ├── voice_processing/
│   │   ├── test_transcription.py
│   │   ├── test_extraction.py
│   │   └── test_synthesis.py
│   ├── price_intelligence/
│   │   ├── test_agmarknet_integration.py
│   │   ├── test_consensus.py
│   │   └── test_fraud_detection.py
│   ├── weather_optimization/
│   │   ├── test_recommendations.py
│   │   └── test_risk_calculation.py
│   ├── freshness_scanner/
│   │   ├── test_classification.py
│   │   └── test_shelf_life.py
│   ├── waste_monetization/
│   │   ├── test_value_calculation.py
│   │   └── test_marketplace.py
│   └── trust_score/
│       ├── test_score_calculation.py
│       └── test_tier_progression.py
├── integration/
│   ├── test_voice_to_database.py
│   ├── test_price_to_whatsapp.py
│   ├── test_offline_sync.py
│   └── test_end_to_end_flows.py
└── property/
    ├── test_voice_properties.py
    ├── test_price_properties.py
    ├── test_weather_properties.py
    ├── test_freshness_properties.py
    ├── test_marketplace_properties.py
    ├── test_trust_score_properties.py
    ├── test_fraud_properties.py
    ├── test_offline_properties.py
    └── test_security_properties.py
```

**Critical Unit Test Cases**:

1. **Voice Processing**:
   - Empty audio input
   - Audio in unsupported language
   - Transaction with missing fields
   - Extremely long audio (>5 minutes)

2. **Price Intelligence**:
   - Zero nearby vendors for consensus
   - All peer prices identical
   - Extreme price outliers (10x normal)
   - Stale cache (>7 days old)

3. **Weather Optimization**:
   - Extreme temperatures (>50°C, <0°C)
   - 100% rain probability
   - New vendor with no history
   - Conflicting weather data sources

4. **Freshness Scanner**:
   - Completely black/white images
   - Multiple produce items in frame
   - Non-produce objects (hands, bags)
   - Very low resolution images

5. **Marketplace**:
   - Zero buyers in radius
   - Buyer and seller at same location
   - Negative residual value
   - Expired listings

6. **Trust Score**:
   - Score at exact tier boundaries
   - Rapid score changes (gaming detection)
   - Long inactivity periods
   - Negative activities (fraud flags)

### Integration Testing

**External API Mocking**:
- Mock Bhashini API responses for consistent testing
- Mock Agmarknet API with realistic price data
- Mock WhatsApp Business API for notification testing
- Mock IMD weather API with various forecast scenarios

**Database Testing**:
- Use PostgreSQL test database with isolated schemas
- Reset database state between tests
- Test transaction isolation and concurrency
- Test migration scripts

**End-to-End Flows**:
1. Complete vendor journey: Registration → Transaction → Price Query → Marketplace
2. Offline-to-online sync: Record offline → Go online → Verify sync
3. Fraud detection flow: Report suspicious price → Validation → Flag → Suspension
4. Trust score progression: Consistent activity → Tier upgrade → Loan eligibility

### Performance Testing

**Load Testing Targets**:
- Voice transcription: <2 seconds for 30-second audio
- Price queries: <3 seconds including Agmarknet API
- Image classification: <5 seconds for 5MB image
- Database queries: <100ms for 95th percentile
- API endpoints: <500ms for 95th percentile

**Stress Testing Scenarios**:
- 1000 concurrent vendors recording transactions
- 10,000 price reports per minute for consensus
- Offline sync of 1000 queued transactions
- Marketplace with 10,000 active listings

**Resource Constraints Testing**:
- Low-end Android device (2GB RAM, quad-core CPU)
- Intermittent 3G connectivity (500ms latency, 20% packet loss)
- Limited storage (500MB available)
- Battery drain monitoring

### Security Testing

**Penetration Testing**:
- SQL injection attempts on all endpoints
- XSS attacks on voice input and marketplace listings
- Authentication bypass attempts
- Rate limiting validation

**Privacy Testing**:
- Verify data anonymization in aggregates
- Test consent enforcement for data sharing
- Validate encryption at rest and in transit
- Test data deletion completeness

**Fraud Testing**:
- Simulate coordinated price manipulation
- Test Isolation Forest with adversarial inputs
- Verify suspension logic with edge cases
- Test reputation recovery mechanisms

### Continuous Integration

**CI Pipeline**:
1. Lint and format checks (Black, ESLint)
2. Unit tests (parallel execution)
3. Property-based tests (100 iterations)
4. Integration tests (sequential)
5. Security scans (Bandit, npm audit)
6. Coverage report generation
7. Performance benchmarks

**Test Execution Time Targets**:
- Unit tests: <5 minutes
- Property tests: <15 minutes
- Integration tests: <10 minutes
- Total CI pipeline: <30 minutes

**Failure Handling**:
- Automatic retry for flaky tests (max 2 retries)
- Detailed failure reports with logs and screenshots
- Slack notifications for test failures
- Block merge if coverage drops below threshold

### Manual Testing

**User Acceptance Testing**:
- Test with actual vendors in Delhi-NCR
- Validate voice recognition with regional accents
- Test in real market conditions (noise, lighting)
- Gather feedback on UI/UX

**Accessibility Testing**:
- Test with low-literacy users
- Validate voice-only interaction flow
- Test with users having visual impairments
- Verify multilingual support quality

**Device Testing**:
- Test on 5+ Android devices (various manufacturers)
- Test on different Android versions (8.0+)
- Test with different screen sizes
- Test with various network conditions


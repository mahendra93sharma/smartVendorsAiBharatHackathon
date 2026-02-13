# Requirements Document: Smart Vendors

## Introduction

Smart Vendors is a voice-first Decision Intelligence application designed for street vendors (rehri-walas) in Delhi-NCR. The system addresses critical business challenges faced by informal sector vendors including inventory loss, information asymmetry, waste management, and financial invisibility. By providing real-time market intelligence, weather-based optimization, and waste monetization capabilities through a zero-typing voice interface, Smart Vendors enables vendors to maximize daily profits while building formal financial credibility.

## Glossary

- **Smart_Mandi_System**: The complete application including voice interface, AI models, and backend services
- **Vendor**: Street vendor (rehri-wala) who sells produce in Delhi-NCR
- **Voice_Ledger**: Voice-based transaction recording system
- **Price_Pulse**: Real-time market price intelligence module
- **Weather_Optimizer**: AI-driven inventory recommendation engine
- **Freshness_Scanner**: Computer vision module for produce quality assessment
- **Waste_Calculator**: Module that monetizes unsold produce
- **Trust_Score**: Credit-building metric based on app usage patterns
- **B_Grade_Marketplace**: Platform for selling downgraded produce
- **Mandi_Credits**: Virtual currency earned through waste monetization
- **Bhashini_API**: Government speech-to-text and translation service
- **Agmarknet**: Official agricultural market price database
- **IMD**: India Meteorological Department
- **Consensus_Algorithm**: Fraud detection system using peer validation
- **Trust_Score_Engine**: Micro-credit scoring system

## Requirements

### Requirement 1: Voice-Based Transaction Recording

**User Story:** As a vendor with low literacy, I want to record sales using voice commands in my native language, so that I can maintain a digital ledger without typing.

#### Acceptance Criteria

1. WHEN a vendor speaks a sales transaction in Hindi, Hinglish, or Bhojpuri, THE Voice_Ledger SHALL convert speech to text using Bhashini_API
2. WHEN the speech-to-text conversion completes, THE Voice_Ledger SHALL extract transaction details (item, quantity, price) using natural language processing
3. WHEN transaction details are extracted, THE Voice_Ledger SHALL store the record in the database with timestamp and vendor ID
4. WHEN a vendor speaks an unclear or ambiguous command, THE Voice_Ledger SHALL request clarification through voice prompts
5. WHEN the Voice_Ledger operates in offline mode, THE Voice_Ledger SHALL queue transactions locally and sync when connectivity returns
6. WHEN a vendor requests their daily summary, THE Voice_Ledger SHALL provide voice playback of total sales, items sold, and remaining inventory

### Requirement 2: Real-Time Market Price Intelligence

**User Story:** As a vendor, I want to know current market prices across Delhi-NCR mandis, so that I can make informed purchasing and pricing decisions.

#### Acceptance Criteria

1. WHEN a vendor queries prices for a specific produce item, THE Price_Pulse SHALL retrieve current rates from Agmarknet within 3 seconds
2. WHEN market prices change by more than 10% for items in the vendor's inventory, THE Price_Pulse SHALL send a voice alert via WhatsApp Business API
3. WHEN displaying price information, THE Price_Pulse SHALL show prices from at least 3 nearby mandis with distance indicators
4. WHEN Agmarknet_API is unavailable, THE Price_Pulse SHALL use cached prices with staleness indicators
5. WHEN a vendor is in a specific location, THE Price_Pulse SHALL prioritize price data from geographically nearest mandis
6. WHEN multiple vendors report prices for the same item and location, THE Price_Pulse SHALL validate using Consensus_Algorithm before displaying

### Requirement 3: Weather-Based Inventory Optimization

**User Story:** As a vendor, I want AI-driven buying recommendations based on weather forecasts, so that I can minimize inventory loss from heat and rain.

#### Acceptance Criteria

1. WHEN the Weather_Optimizer runs each morning at 5 AM, THE Weather_Optimizer SHALL fetch IMD weather forecasts for the vendor's location
2. WHEN temperature is predicted to exceed 42°C, THE Weather_Optimizer SHALL recommend reducing heat-sensitive produce purchases by 15-25%
3. WHEN rain is predicted with >70% probability, THE Weather_Optimizer SHALL recommend reducing leafy vegetable purchases by 20-30%
4. WHEN weather conditions are optimal, THE Weather_Optimizer SHALL recommend standard or increased purchasing based on historical demand
5. WHEN generating recommendations, THE Weather_Optimizer SHALL consider the vendor's historical sales patterns and current inventory levels
6. WHEN the vendor requests explanation for a recommendation, THE Weather_Optimizer SHALL provide voice-based reasoning in the vendor's preferred language

### Requirement 4: Computer Vision Freshness Assessment

**User Story:** As a vendor, I want to assess produce freshness by taking photos, so that I can categorize items for optimal pricing and waste reduction.

#### Acceptance Criteria

1. WHEN a vendor captures a photo of produce, THE Freshness_Scanner SHALL classify it into Fresh, B-Grade, or Waste categories using YOLOv8 model
2. WHEN produce is classified as Fresh, THE Freshness_Scanner SHALL estimate remaining shelf life in hours based on visual indicators
3. WHEN produce is classified as B-Grade, THE Freshness_Scanner SHALL suggest alternative uses (juice, pickle, animal feed)
4. WHEN produce is classified as Waste, THE Freshness_Scanner SHALL recommend composting options with nearby facility locations
5. WHEN the image quality is insufficient for classification, THE Freshness_Scanner SHALL request a clearer photo with voice guidance
6. WHEN classification confidence is below 70%, THE Freshness_Scanner SHALL display confidence score and request manual verification

### Requirement 5: Waste Monetization Marketplace

**User Story:** As a vendor, I want to sell downgraded produce to juice stalls and pickle makers, so that I can recover value from unsold inventory.

#### Acceptance Criteria

1. WHEN a vendor lists B-Grade produce, THE Waste_Calculator SHALL compute residual value using formula V_residual = (W × C_rate) - L_fee
2. WHEN B-Grade produce is listed, THE B_Grade_Marketplace SHALL notify nearby buyers (juice stalls, pickle makers) within 5km radius
3. WHEN a buyer expresses interest, THE B_Grade_Marketplace SHALL facilitate connection via WhatsApp with pickup location and time
4. WHEN a transaction completes, THE Waste_Calculator SHALL credit Mandi_Credits to the vendor's account
5. WHEN no buyers are found within 2 hours, THE B_Grade_Marketplace SHALL suggest composting facilities with pickup logistics
6. WHEN Mandi_Credits accumulate, THE Waste_Calculator SHALL display conversion rate to rupees and redemption options

### Requirement 6: Micro-Credit Building System

**User Story:** As a vendor, I want to build a digital credit history through app usage, so that I can access formal banking services and PM-SVANidhi loans.

#### Acceptance Criteria

1. WHEN a vendor records transactions consistently, THE Trust_Score_Engine SHALL increment their Trust_Score based on frequency and accuracy
2. WHEN a vendor's Trust_Score reaches threshold levels (Bronze: 100, Silver: 250, Gold: 500), THE Trust_Score_Engine SHALL unlock corresponding benefits
3. WHEN a vendor requests loan eligibility information, THE Trust_Score_Engine SHALL generate a PM-SVANidhi compatibility report
4. WHEN the Trust_Score_Engine calculates scores, THE Trust_Score_Engine SHALL consider transaction volume, consistency, waste reduction, and marketplace participation
5. WHEN a vendor shares their Trust_Score with financial institutions, THE Smart_Mandi_System SHALL generate a verifiable digital certificate
6. WHEN Trust_Score decreases due to inactivity, THE Trust_Score_Engine SHALL send reminder notifications to maintain engagement

### Requirement 7: Fraud Prevention and Price Validation

**User Story:** As a system administrator, I want to detect and prevent fraudulent price reporting, so that the marketplace maintains trust and accuracy.

#### Acceptance Criteria

1. WHEN a vendor reports a price, THE Consensus_Algorithm SHALL compare it against reports from at least 3 nearby vendors within 2km radius
2. WHEN a reported price deviates by more than 25% from peer consensus, THE Consensus_Algorithm SHALL flag it for review
3. WHEN the Consensus_Algorithm detects anomalies, THE Consensus_Algorithm SHALL use Isolation Forest ML model to classify as genuine outlier or fraud
4. WHEN fraud is detected with >80% confidence, THE Smart_Mandi_System SHALL exclude the price from public display and notify the vendor
5. WHEN a vendor has 3 or more fraud flags, THE Smart_Mandi_System SHALL temporarily suspend their price reporting privileges
6. WHEN Agmarknet_API data is available, THE Consensus_Algorithm SHALL cross-reference vendor reports with official rates as additional validation

### Requirement 8: Offline-First Mobile Experience

**User Story:** As a vendor with unreliable internet connectivity, I want the app to work offline, so that I can continue recording transactions and accessing cached information.

#### Acceptance Criteria

1. WHEN the Smart_Mandi_System detects no internet connectivity, THE Smart_Mandi_System SHALL enable offline mode with visual indicator
2. WHILE in offline mode, THE Voice_Ledger SHALL store transactions locally using device storage
3. WHEN connectivity is restored, THE Smart_Mandi_System SHALL sync all queued transactions to the server within 30 seconds
4. WHILE in offline mode, THE Price_Pulse SHALL display last cached prices with timestamp showing data age
5. WHEN critical features require connectivity (price updates, marketplace listings), THE Smart_Mandi_System SHALL queue actions and notify vendor when sync completes
6. WHEN sync conflicts occur (same transaction recorded offline and online), THE Smart_Mandi_System SHALL use timestamp-based resolution with vendor notification

### Requirement 9: Multilingual Voice Interface

**User Story:** As a vendor who speaks Hindi, Hinglish, or Bhojpuri, I want the app to understand and respond in my preferred language, so that I can use it comfortably without language barriers.

#### Acceptance Criteria

1. WHEN a vendor first launches the app, THE Smart_Mandi_System SHALL detect language preference through voice sample or manual selection
2. WHEN the vendor speaks in their chosen language, THE Voice_Ledger SHALL maintain conversation context across multiple exchanges
3. WHEN translating between languages, THE Smart_Mandi_System SHALL preserve business terminology (mandi, kilo, bhav) without translation
4. WHEN voice recognition confidence is below 60%, THE Smart_Mandi_System SHALL request repetition with clearer pronunciation guidance
5. WHEN the vendor switches languages mid-conversation, THE Smart_Mandi_System SHALL detect the change and adapt within 2 exchanges
6. WHEN providing voice responses, THE Smart_Mandi_System SHALL use natural speech patterns appropriate for the vendor's language and region

### Requirement 10: WhatsApp Business Integration

**User Story:** As a vendor who primarily uses WhatsApp, I want to receive alerts and interact with the system through WhatsApp, so that I don't need to learn a new interface.

#### Acceptance Criteria

1. WHEN a vendor registers, THE Smart_Mandi_System SHALL link their WhatsApp number for notifications
2. WHEN price alerts or weather warnings are generated, THE Smart_Mandi_System SHALL send messages via WhatsApp Business API within 1 minute
3. WHEN a vendor sends a WhatsApp message with a query, THE Smart_Mandi_System SHALL process it and respond within 5 seconds
4. WHEN marketplace transactions occur, THE Smart_Mandi_System SHALL facilitate buyer-seller communication through WhatsApp with privacy protection
5. WHEN the vendor opts out of specific notification types, THE Smart_Mandi_System SHALL respect preferences while maintaining critical alerts
6. WHEN WhatsApp Business API is unavailable, THE Smart_Mandi_System SHALL fall back to SMS for critical notifications

### Requirement 11: Demand Prediction and Dynamic Pricing

**User Story:** As a vendor, I want AI-driven demand predictions for my location, so that I can adjust prices dynamically and maximize revenue.

#### Acceptance Criteria

1. WHEN the Smart_Mandi_System analyzes demand patterns, THE Smart_Mandi_System SHALL use Random Forest model trained on historical sales, weather, and local events
2. WHEN demand for an item is predicted to be high, THE Smart_Mandi_System SHALL suggest price increases of 5-15% with confidence scores
3. WHEN demand is predicted to be low, THE Smart_Mandi_System SHALL recommend promotional pricing or alternative sales channels
4. WHEN generating predictions, THE Smart_Mandi_System SHALL consider day of week, festivals, weather, and neighborhood demographics
5. WHEN prediction accuracy falls below 70%, THE Smart_Mandi_System SHALL retrain the model using recent transaction data
6. WHEN a vendor consistently ignores recommendations, THE Smart_Mandi_System SHALL adapt suggestions based on the vendor's actual pricing behavior

### Requirement 12: Data Privacy and Security

**User Story:** As a vendor, I want my transaction data to be secure and private, so that my business information is protected from competitors and misuse.

#### Acceptance Criteria

1. WHEN a vendor registers, THE Smart_Mandi_System SHALL encrypt all personal and transaction data using AES-256 encryption
2. WHEN storing data, THE Smart_Mandi_System SHALL anonymize vendor identities in aggregate analytics and marketplace listings
3. WHEN sharing data with third parties (banks, government), THE Smart_Mandi_System SHALL require explicit vendor consent
4. WHEN a vendor requests data deletion, THE Smart_Mandi_System SHALL remove all personal information within 30 days while preserving anonymized analytics
5. WHEN authentication is required, THE Smart_Mandi_System SHALL use OTP-based verification via SMS or WhatsApp
6. WHEN detecting suspicious access patterns, THE Smart_Mandi_System SHALL lock the account and notify the vendor immediately

---

## Notes

- All voice interactions should prioritize simplicity and use familiar terminology from the vendor's daily business context
- The system must be optimized for low-end Android devices (2GB RAM, intermittent 3G connectivity)
- Performance targets: Voice recognition <2s, Price queries <3s, Image classification <5s
- The application should consume minimal battery and data to accommodate vendors' resource constraints
- Cultural sensitivity is critical - avoid terminology or interactions that might alienate low-literacy users

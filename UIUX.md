# UI/UX Design Document: Smart Vendors

## Design Link
**Google Stitch Project:** https://stitch.withgoogle.com/u/2/projects/2694440529550789027

---

## Design Philosophy

Smart Vendors follows a **voice-first, zero-typing** design philosophy tailored for street vendors (rehri-walas) in Delhi-NCR with low literacy levels and limited smartphone experience. The interface prioritizes:

- **Voice-driven interactions** over text input
- **Large, icon-based navigation** for easy recognition
- **Minimal cognitive load** with single-task focused screens
- **Offline-first experience** with clear connectivity indicators
- **Multilingual support** (Hindi, Hinglish, Bhojpuri)
- **Low-resource optimization** for 2GB RAM devices with 3G connectivity

---

## Target User Profile

- **Demographics:** Street vendors aged 25-55, primarily male
- **Literacy Level:** Low to moderate (5th-8th grade equivalent)
- **Language:** Hindi, Hinglish, or Bhojpuri speakers
- **Device:** Low-end Android smartphones (2GB RAM, intermittent 3G)
- **Tech Familiarity:** Basic WhatsApp usage, limited app experience
- **Daily Context:** 12-14 hour workdays, hands busy with customers, noisy street environment

---

## Core User Flows

### 1. Voice Transaction Recording Flow
**User Goal:** Record a sale without typing

**Steps:**
1. Vendor taps large microphone button on home screen
2. Voice prompt: "Kya becha?" (What did you sell?)
3. Vendor speaks: "Do kilo tamatar, pachas rupaye"
4. System confirms: "2 kg tomatoes, ₹50 - Sahi hai?" (Correct?)
5. Vendor confirms with voice "Haan" or tap checkmark
6. Transaction saved with success animation

**Design Considerations:**
- Microphone button occupies 40% of screen (easy to tap)
- Visual waveform feedback during speech
- Clear confirmation before saving
- Offline queue indicator if no connectivity

---

### 2. Market Price Check Flow
**User Goal:** Check current mandi prices before purchasing

**Steps:**
1. Vendor taps "Price Pulse" icon (rupee symbol)
2. Voice prompt: "Kis cheez ka bhav chahiye?" (Which item's price?)
3. Vendor speaks item name or selects from recent items
4. System displays prices from 3 nearby mandis with distance
5. Price alert option: "Bhav badalne par batao?" (Alert on price change?)

**Design Considerations:**
- Large price numbers (48pt font)
- Color coding: Green (low), Yellow (medium), Red (high)
- Distance shown in km with map icon
- Comparison with yesterday's price (↑↓ indicators)

---

### 3. Freshness Scanner Flow
**User Goal:** Assess produce quality to decide pricing

**Steps:**
1. Vendor taps camera icon on home screen
2. Camera opens with overlay guide (circular frame)
3. Vendor captures photo of produce
4. System analyzes and shows result:
   - **Fresh:** Green badge, estimated shelf life
   - **B-Grade:** Yellow badge, suggested uses (juice, pickle)
   - **Waste:** Red badge, composting options
5. Option to list B-Grade items on marketplace

**Design Considerations:**
- Camera guide shows ideal framing
- Large result badges with icons (no text-heavy explanations)
- Voice readout of classification result
- One-tap marketplace listing from B-Grade result

---

### 4. Weather-Based Buying Recommendation Flow
**User Goal:** Get AI advice on what to buy today

**Steps:**
1. Morning notification (5 AM): "Aaj ka mausam dekho" (Check today's weather)
2. Vendor opens Weather Optimizer
3. Screen shows:
   - Weather icon (sun/rain/cloud) with temperature
   - Recommendation: "Patte wali sabzi kam lo" (Buy less leafy vegetables)
   - Reason (voice): "Aaj baarish hogi, patte jaldi kharab hote hain"
4. Vendor can tap "Kyun?" (Why?) for detailed voice explanation

**Design Considerations:**
- Large weather icon dominates screen
- Recommendation in simple Hindi/Hinglish
- Color-coded advice: Red (reduce), Green (increase), Yellow (normal)
- Voice explanation on demand (not forced)

---

### 5. Trust Score & Credit Building Flow
**User Goal:** Track progress toward loan eligibility

**Steps:**
1. Vendor taps profile icon
2. Trust Score displayed as progress bar with tier badge:
   - Bronze (100 points)
   - Silver (250 points)
   - Gold (500 points)
3. Points breakdown shown with icons:
   - Transaction consistency
   - Waste reduction
   - Marketplace participation
4. "PM-SVANidhi ke liye taiyar?" (Ready for PM-SVANidhi?) button
5. Generates shareable certificate for bank

**Design Considerations:**
- Gamified progress bar with celebratory animations
- Tier badges use familiar symbols (bronze/silver/gold colors)
- Simple point breakdown (no complex charts)
- One-tap certificate generation

---

## Screen Inventory

### Primary Screens
1. **Home Dashboard**
   - Large microphone button (voice transaction)
   - Quick access icons: Price Pulse, Freshness Scanner, Weather
   - Daily summary card (sales, inventory)
   - Trust Score widget

2. **Voice Ledger**
   - Transaction recording interface
   - Daily/weekly transaction list
   - Voice playback of summaries

3. **Price Pulse**
   - Market price comparison
   - Price alerts management
   - Historical price trends (simple line graph)

4. **Weather Optimizer**
   - Weather forecast display
   - Buying recommendations
   - Historical accuracy tracker

5. **Freshness Scanner**
   - Camera interface with guide
   - Classification results
   - B-Grade marketplace listing

6. **B-Grade Marketplace**
   - Vendor's listings
   - Nearby buyer notifications
   - Mandi Credits balance

7. **Trust Score Profile**
   - Score progress and tier
   - Points breakdown
   - PM-SVANidhi certificate

8. **Settings**
   - Language preference
   - Notification preferences
   - Data sync status
   - Privacy controls

---

## Visual Design System

### Color Palette
- **Primary:** #FF6B35 (Vibrant Orange - energy, warmth)
- **Secondary:** #4ECDC4 (Teal - trust, freshness)
- **Success:** #95E1D3 (Light Green - positive actions)
- **Warning:** #F7DC6F (Yellow - caution, attention)
- **Error:** #E74C3C (Red - alerts, waste)
- **Background:** #F8F9FA (Light Gray - clean, minimal)
- **Text Primary:** #2C3E50 (Dark Blue-Gray - readability)
- **Text Secondary:** #7F8C8D (Medium Gray - supporting text)

### Typography
- **Primary Font:** Noto Sans Devanagari (Hindi support)
- **Fallback:** Roboto (Latin characters)
- **Sizes:**
  - Headings: 24-32pt (bold)
  - Body: 18-20pt (regular)
  - Prices/Numbers: 36-48pt (bold)
  - Captions: 14-16pt (regular)

### Iconography
- **Style:** Filled, rounded corners (friendly, approachable)
- **Size:** Minimum 48x48dp (easy tap targets)
- **Icons:**
  - Microphone (voice input)
  - Rupee symbol (prices)
  - Camera (freshness scanner)
  - Cloud/sun/rain (weather)
  - Trophy (trust score)
  - WhatsApp logo (notifications)

### Spacing & Layout
- **Minimum tap target:** 48x48dp (accessibility standard)
- **Padding:** 16-24dp between elements
- **Card elevation:** 2-4dp (subtle depth)
- **Screen margins:** 16dp (comfortable reading)

---

## Accessibility Features

### Voice Interface
- **Speech-to-text:** Bhashini API for Hindi/Hinglish/Bhojpuri
- **Text-to-speech:** Voice feedback for all actions
- **Wake word:** Optional "Hey Smart Mandi" activation
- **Noise cancellation:** Background noise filtering for street environment

### Visual Accessibility
- **High contrast mode:** For outdoor visibility
- **Large text option:** 150% scaling
- **Color-blind friendly:** Icons don't rely solely on color
- **Screen reader support:** TalkBack compatibility

### Low-Literacy Design
- **Icon-first navigation:** Minimal text labels
- **Voice labels:** Every button has voice description
- **Confirmation dialogs:** Always confirm before destructive actions
- **Undo option:** Recent actions can be reversed

---

## Offline-First Design

### Connectivity Indicators
- **Online:** Green dot in status bar
- **Offline:** Orange dot with "Offline" badge
- **Syncing:** Animated blue dot with progress

### Offline Capabilities
- **Voice transactions:** Queued locally, synced when online
- **Price data:** Last cached prices shown with timestamp
- **Freshness scanner:** Works offline (model on-device)
- **Marketplace:** Listings queued for upload

### Sync Behavior
- **Auto-sync:** When connectivity restored
- **Manual sync:** Pull-to-refresh gesture
- **Conflict resolution:** Timestamp-based with user notification
- **Sync status:** Clear progress indicator

---

## Performance Optimization

### Load Times
- **App launch:** <2 seconds (cold start)
- **Voice recognition:** <2 seconds (speech-to-text)
- **Price queries:** <3 seconds (API fetch)
- **Image classification:** <5 seconds (YOLOv8 inference)

### Resource Management
- **Battery:** Background services minimized
- **Data usage:** Images compressed, API calls batched
- **Storage:** Local cache limited to 100MB
- **Memory:** Optimized for 2GB RAM devices

---

## Localization Strategy

### Language Support
- **Hindi:** Primary language (Devanagari script)
- **Hinglish:** Mixed Hindi-English (Latin script)
- **Bhojpuri:** Regional dialect support

### Cultural Considerations
- **Terminology:** Use familiar market terms (mandi, bhav, kilo)
- **Currency:** Always show ₹ symbol with amounts
- **Date/Time:** 12-hour format (common in India)
- **Units:** Metric system (kg, liters)

### Voice Adaptation
- **Accent recognition:** Delhi-NCR regional accents
- **Code-switching:** Handle Hindi-English mixing
- **Slang:** Recognize common market slang terms

---

## Interaction Patterns

### Primary Actions
- **Voice input:** Large microphone button (always visible)
- **Quick actions:** Swipe gestures for common tasks
- **Confirmation:** Two-step for critical actions (delete, share)

### Feedback Mechanisms
- **Visual:** Color changes, animations, badges
- **Auditory:** Voice confirmations, success sounds
- **Haptic:** Vibration for button presses (optional)

### Error Handling
- **Voice errors:** "Samajh nahi aaya, phir se bolo" (Didn't understand, say again)
- **Network errors:** "Internet nahi hai, baad mein sync hoga" (No internet, will sync later)
- **Camera errors:** "Photo saaf nahi hai, phir se lo" (Photo unclear, take again)

---

## WhatsApp Integration Design

### Notification Templates
- **Price alerts:** "🔔 Tamatar ka bhav badh gaya! Azadpur: ₹40/kg"
- **Weather warnings:** "⚠️ Aaj baarish hogi. Patte wali sabzi kam lo."
- **Marketplace:** "🛒 Koi aapke aam kharidna chahta hai. Dekho?"
- **Trust Score:** "🏆 Badhai! Aap Silver level par pahunch gaye!"

### Interactive Messages
- **Quick replies:** Pre-defined buttons for common responses
- **Voice notes:** Vendors can reply with voice messages
- **Image sharing:** Freshness scanner results via WhatsApp

---

## Design Validation

### Usability Testing Plan
1. **Prototype testing:** 5 vendors test key flows
2. **Voice accuracy:** Test in noisy street environment
3. **Offline scenarios:** Simulate connectivity loss
4. **Literacy testing:** Observe icon recognition
5. **Performance:** Test on low-end devices (2GB RAM)

### Success Metrics
- **Task completion rate:** >90% for primary flows
- **Voice recognition accuracy:** >85% in street noise
- **Time to complete transaction:** <30 seconds
- **User satisfaction:** >4/5 rating
- **Daily active usage:** >70% of registered vendors

---

## Future Enhancements

### Phase 2 Features
- **AR freshness overlay:** Real-time camera overlay for quality
- **Voice assistant:** Conversational AI for complex queries
- **Social features:** Vendor community and tips sharing
- **Gamification:** Badges, leaderboards for engagement

### Advanced Personalization
- **Adaptive UI:** Learn vendor's preferred workflows
- **Smart suggestions:** Predict next action based on time/context
- **Custom shortcuts:** Vendor-defined quick actions

---

## Design Assets Location

**Google Stitch Project:** https://stitch.withgoogle.com/u/2/projects/2694440529550789027

### Asset Inventory
- [ ] Wireframes (all primary screens)
- [ ] High-fidelity mockups
- [ ] Interactive prototype
- [ ] Icon set (SVG format)
- [ ] Color palette swatches
- [ ] Typography specimens
- [ ] Component library
- [ ] Animation specifications
- [ ] Voice interaction flows
- [ ] Accessibility annotations

---

## Notes

- All designs prioritize voice-first interaction over visual complexity
- Icons and colors must work in bright outdoor sunlight
- Test all flows with actual vendors in street environment
- Ensure designs work on smallest supported screen size (4.5" display)
- Voice prompts should be conversational, not robotic
- Avoid technical jargon - use everyday market language

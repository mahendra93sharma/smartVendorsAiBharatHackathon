# Smart Vendors - Manual Testing Checklist

## Frontend Running: ✅ http://localhost:3000

## Test Instructions

Open your browser and navigate to: **http://localhost:3000**

---

## 1. Home Dashboard (Requirement 1.3, 1.4)

### Tests:
- [ ] Page loads successfully
- [ ] Large microphone button visible (40% of screen)
- [ ] Quick access cards displayed:
  - [ ] Price Pulse
  - [ ] Freshness Scanner
  - [ ] Marketplace
  - [ ] Trust Score
- [ ] Daily summary widget visible
- [ ] Responsive on mobile (resize browser to 320px-768px)
- [ ] Demo mode toggle visible

**Expected Result:** Clean, mobile-first dashboard with all navigation cards

---

## 2. Voice Transaction Recording (Requirement 5.1)

### Tests:
- [ ] Click microphone button on home
- [ ] Voice transaction page loads
- [ ] Large circular microphone button visible
- [ ] Click to start recording
- [ ] Waveform animation appears
- [ ] Recording timer shows
- [ ] Click to stop recording
- [ ] Transcription result displays
- [ ] Transaction details extracted:
  - [ ] Item name
  - [ ] Quantity
  - [ ] Unit
  - [ ] Price per unit
  - [ ] Total amount
- [ ] Confidence indicator shown
- [ ] "Confirm" and "Re-record" buttons work

**Expected Result:** Demo mode shows pre-recorded sample with extracted transaction

---

## 3. Market Price Intelligence (Requirement 5.2)

### Tests:
- [ ] Navigate to Price Intelligence
- [ ] Search input field visible
- [ ] Voice input button available
- [ ] Enter "tomatoes" and search
- [ ] Price comparison table displays
- [ ] Shows 3 mandis:
  - [ ] Azadpur Mandi
  - [ ] Ghazipur Mandi
  - [ ] Okhla Mandi
- [ ] Each row shows:
  - [ ] Mandi name
  - [ ] Price per kg
  - [ ] Distance in km
  - [ ] Price trend indicator (↑↓→)
- [ ] Color coding:
  - [ ] Green for low prices
  - [ ] Yellow for medium prices
  - [ ] Red for high prices
- [ ] Legend explains color coding

**Expected Result:** Price comparison from 3 mandis with color-coded pricing

---

## 4. Freshness Scanner (Requirement 5.3)

### Tests:
- [ ] Navigate to Freshness Scanner
- [ ] Camera interface visible
- [ ] Circular overlay guide shown
- [ ] "Capture" or "Upload" button available
- [ ] Upload/capture image
- [ ] Classification result displays:
  - [ ] Category (Fresh/B-Grade/Waste)
  - [ ] Color-coded badge (Green/Yellow/Red)
  - [ ] Confidence score
- [ ] For Fresh: Shelf life estimate shown
- [ ] For B-Grade: Suggestions displayed (juice, pickle)
- [ ] For B-Grade: "List on Marketplace" button visible
- [ ] For Waste: Disposal suggestions shown (compost)

**Expected Result:** Image classification with category, confidence, and suggestions

---

## 5. Marketplace (Requirement 5.4)

### Tests:
- [ ] Navigate to Marketplace
- [ ] Listing form visible with fields:
  - [ ] Item name
  - [ ] Weight (kg)
  - [ ] Price
- [ ] "Create Listing" button works
- [ ] Active listings displayed
- [ ] Nearby buyers count shown
- [ ] Notification status visible
- [ ] Mandi Credits balance displayed
- [ ] Tier badge shown (Bronze/Silver/Gold)
- [ ] Credits calculation: 10 credits per kg

**Expected Result:** Marketplace for B-Grade produce with credit system

---

## 6. Trust Score Profile (Requirement 5.5)

### Tests:
- [ ] Navigate to Trust Score
- [ ] Trust Score displayed as progress bar
- [ ] Current score shown
- [ ] Next tier threshold visible
- [ ] Tier badge displayed (Bronze/Silver/Gold)
- [ ] Score breakdown shown:
  - [ ] Transactions count
  - [ ] Marketplace sales
  - [ ] Consistency score
- [ ] Tier logic:
  - [ ] Bronze: 0-99
  - [ ] Silver: 100-249
  - [ ] Gold: 250+
- [ ] "Share Certificate" button visible

**Expected Result:** Trust score visualization with tier progression

---

## 7. Demo Mode (Requirement 9.3, 9.4)

### Tests:
- [ ] Demo mode toggle on home page
- [ ] Toggle switches between demo/live mode
- [ ] Demo mode indicator visible when active
- [ ] Pre-recorded audio samples work
- [ ] Mock data displays correctly
- [ ] Tutorial overlay available
- [ ] Step-by-step walkthrough works
- [ ] LocalStorage used for offline queue

**Expected Result:** Demo mode with pre-recorded samples and tutorial

---

## 8. Mobile Responsiveness (Requirement 1.4)

### Tests:
- [ ] Resize browser to 320px width
- [ ] All content visible (no horizontal scroll)
- [ ] Touch targets ≥ 44x44 pixels
- [ ] Text readable at small sizes
- [ ] Buttons easily tappable
- [ ] Resize to 768px width
- [ ] Layout adapts appropriately
- [ ] Test on actual mobile device if possible

**Expected Result:** Fully responsive on 320px-768px screens

---

## 9. Navigation & UX

### Tests:
- [ ] Back button works on all pages
- [ ] Navigation between pages smooth
- [ ] Loading states shown
- [ ] Error messages clear and helpful
- [ ] Success messages displayed
- [ ] Offline mode queues transactions
- [ ] Demo credentials visible:
  - [ ] Username: demo_vendor
  - [ ] Password: hackathon2024

**Expected Result:** Smooth navigation with clear feedback

---

## 10. Performance (Requirement 1.2)

### Tests:
- [ ] Initial page load < 3 seconds
- [ ] Navigation between pages instant
- [ ] No console errors
- [ ] Images load properly
- [ ] Animations smooth
- [ ] No memory leaks (check DevTools)

**Expected Result:** Fast, smooth performance

---

## Backend API Tests (When Available)

### API Endpoints:
1. `POST /voice/transcribe` - Voice transcription
2. `POST /transactions` - Create transaction
3. `GET /transactions/{vendor_id}` - Get transactions
4. `GET /prices/{item}` - Market prices
5. `POST /freshness/classify` - Freshness classification
6. `POST /marketplace/listings` - Create listing
7. `GET /marketplace/buyers` - Get buyers
8. `POST /marketplace/notify` - Notify buyers
9. `GET /trust-score/{vendor_id}` - Trust score

### Tests:
- [ ] All endpoints respond
- [ ] Response times < 2 seconds
- [ ] Error handling works
- [ ] Demo data returns correctly

---

## Code Quality Checks

### Frontend:
- [x] ESLint passes: `npm run lint`
- [x] TypeScript compiles: `npx tsc --noEmit`
- [x] Tests pass: `npm test`
- [x] Build succeeds: `npm run build`
- [x] Prettier formatted: `npm run format`

### Backend:
- [x] Black formatted: `python -m black . --check`
- [x] Tests pass: `pytest tests/ -v`
- [x] Type hints present
- [x] Error handling implemented

---

## Documentation Checks

- [x] README.md complete with:
  - [x] Project overview
  - [x] Problem statement
  - [x] Solution description
  - [x] Architecture diagram
  - [x] AWS services listed
  - [x] Demo credentials
  - [x] Setup instructions
- [x] API documentation (docs/API.md)
- [x] Architecture documentation (docs/ARCHITECTURE.md)
- [x] Deployment guide (docs/DEPLOYMENT.md)
- [x] CONTRIBUTING.md
- [x] LICENSE
- [x] .gitignore
- [x] .env.example

---

## AWS Services Verification

### Services Used:
- [x] Amazon Bedrock - NLP and decision intelligence
- [x] AWS Lambda - Serverless compute (9 functions)
- [x] Amazon S3 - Object storage
- [x] Amazon DynamoDB - NoSQL database
- [x] Amazon SageMaker - ML inference
- [x] AWS Transcribe - Voice-to-text
- [x] API Gateway - API routing
- [x] CloudFront - CDN (optional)

---

## Deployment Readiness

- [x] docker-compose.yml configured
- [x] setup.sh script created
- [x] Lambda deployment script ready
- [x] Frontend Dockerfile ready
- [x] Backend Dockerfile ready
- [x] Environment variables documented
- [x] Deployment checklist created
- [x] Submission checklist created

---

## Final Checks

- [ ] All features work in demo mode
- [ ] No console errors
- [ ] Mobile responsive
- [ ] Performance acceptable
- [ ] Documentation complete
- [ ] Code formatted and linted
- [ ] Tests passing
- [ ] Ready for AWS deployment

---

## Test Results Summary

**Date:** _________________

**Tester:** _________________

**Overall Status:** ⬜ Pass  ⬜ Fail  ⬜ Needs Work

**Notes:**
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

**Issues Found:**
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

**Recommendations:**
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

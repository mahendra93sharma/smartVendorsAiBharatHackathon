#!/bin/bash

# iOS Setup Verification Script
# This script verifies that the iOS build environment is properly configured

set -e

echo "🔍 Verifying iOS Build Setup..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check functions
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✅ $1 is installed${NC}"
        return 0
    else
        echo -e "${RED}❌ $1 is not installed${NC}"
        return 1
    fi
}

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅ $1 exists${NC}"
        return 0
    else
        echo -e "${RED}❌ $1 not found${NC}"
        return 1
    fi
}

check_directory() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✅ $1 exists${NC}"
        return 0
    else
        echo -e "${RED}❌ $1 not found${NC}"
        return 1
    fi
}

# Track overall status
ERRORS=0

echo "📦 Checking Prerequisites..."
echo ""

# Check macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "${GREEN}✅ Running on macOS${NC}"
else
    echo -e "${RED}❌ iOS development requires macOS${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Check Xcode
if check_command xcodebuild; then
    XCODE_VERSION=$(xcodebuild -version | head -n 1)
    echo "   Version: $XCODE_VERSION"
else
    echo -e "${YELLOW}   Install from: https://developer.apple.com/xcode/${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Check CocoaPods
if check_command pod; then
    POD_VERSION=$(pod --version)
    echo "   Version: $POD_VERSION"
else
    echo -e "${YELLOW}   Install with: sudo gem install cocoapods${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Check Node.js
if check_command node; then
    NODE_VERSION=$(node --version)
    echo "   Version: $NODE_VERSION"
    
    # Check if version is >= 18
    NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1 | sed 's/v//')
    if [ "$NODE_MAJOR" -ge 18 ]; then
        echo -e "${GREEN}   ✅ Node.js version is sufficient${NC}"
    else
        echo -e "${YELLOW}   ⚠️  Node.js 18+ recommended${NC}"
    fi
else
    echo -e "${YELLOW}   Install from: https://nodejs.org/${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Check npm
if check_command npm; then
    NPM_VERSION=$(npm --version)
    echo "   Version: $NPM_VERSION"
else
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "📁 Checking Project Files..."
echo ""

# Check Podfile
check_file "Podfile" || ERRORS=$((ERRORS + 1))

# Check Info.plist
check_file "VendorApp/Info.plist" || ERRORS=$((ERRORS + 1))

# Check if Pods are installed
if check_directory "Pods"; then
    echo -e "${GREEN}   ✅ CocoaPods dependencies installed${NC}"
else
    echo -e "${YELLOW}   ⚠️  Run 'pod install' to install dependencies${NC}"
fi

# Check for workspace
if check_file "VendorApp.xcworkspace"; then
    echo -e "${GREEN}   ✅ Xcode workspace exists${NC}"
else
    echo -e "${YELLOW}   ⚠️  Run 'pod install' to generate workspace${NC}"
fi

echo ""
echo "🔐 Checking Permissions in Info.plist..."
echo ""

# Check permission descriptions
PLIST_FILE="VendorApp/Info.plist"
if [ -f "$PLIST_FILE" ]; then
    PERMISSIONS=(
        "NSCameraUsageDescription"
        "NSMicrophoneUsageDescription"
        "NSLocationWhenInUseUsageDescription"
        "NSPhotoLibraryUsageDescription"
    )
    
    for PERMISSION in "${PERMISSIONS[@]}"; do
        if grep -q "$PERMISSION" "$PLIST_FILE"; then
            echo -e "${GREEN}✅ $PERMISSION configured${NC}"
        else
            echo -e "${RED}❌ $PERMISSION missing${NC}"
            ERRORS=$((ERRORS + 1))
        fi
    done
else
    echo -e "${RED}❌ Info.plist not found${NC}"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "📱 Checking iOS Simulators..."
echo ""

if check_command xcrun; then
    SIMULATOR_COUNT=$(xcrun simctl list devices available | grep -c "iPhone" || true)
    if [ "$SIMULATOR_COUNT" -gt 0 ]; then
        echo -e "${GREEN}✅ $SIMULATOR_COUNT iPhone simulators available${NC}"
        echo ""
        echo "Available simulators:"
        xcrun simctl list devices available | grep "iPhone" | head -5
    else
        echo -e "${YELLOW}⚠️  No iPhone simulators found${NC}"
        echo "   Install simulators from Xcode → Preferences → Components"
    fi
fi

echo ""
echo "📋 Configuration Summary..."
echo ""

# Check Podfile configuration
if [ -f "Podfile" ]; then
    if grep -q "platform :ios, '12.0'" "Podfile"; then
        echo -e "${GREEN}✅ iOS 12.0 minimum version configured${NC}"
    else
        echo -e "${YELLOW}⚠️  iOS version not set to 12.0${NC}"
    fi
    
    if grep -q "react-native-camera" "Podfile"; then
        echo -e "${GREEN}✅ Camera dependency configured${NC}"
    else
        echo -e "${YELLOW}⚠️  Camera dependency missing${NC}"
    fi
    
    if grep -q "react-native-voice" "Podfile"; then
        echo -e "${GREEN}✅ Voice dependency configured${NC}"
    else
        echo -e "${YELLOW}⚠️  Voice dependency missing${NC}"
    fi
    
    if grep -q "react-native-geolocation" "Podfile"; then
        echo -e "${GREEN}✅ Geolocation dependency configured${NC}"
    else
        echo -e "${YELLOW}⚠️  Geolocation dependency missing${NC}"
    fi
fi

echo ""
echo "🎯 Next Steps..."
echo ""

if [ ! -d "Pods" ]; then
    echo "1. Install CocoaPods dependencies:"
    echo "   cd ios && pod install && cd .."
    echo ""
fi

if [ ! -f "VendorApp.xcworkspace" ]; then
    echo "2. Generate Xcode workspace:"
    echo "   cd ios && pod install && cd .."
    echo ""
fi

echo "3. Open workspace in Xcode:"
echo "   open ios/VendorApp.xcworkspace"
echo ""

echo "4. Configure code signing in Xcode:"
echo "   - Select VendorApp target"
echo "   - Go to Signing & Capabilities"
echo "   - Enable 'Automatically manage signing'"
echo "   - Select your team"
echo ""

echo "5. Run on simulator:"
echo "   npm run ios"
echo ""

echo "═══════════════════════════════════════════════════════════"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ Setup verification complete! No errors found.${NC}"
else
    echo -e "${YELLOW}⚠️  Setup verification complete with $ERRORS issue(s).${NC}"
    echo "Please address the issues above before building."
fi
echo "═══════════════════════════════════════════════════════════"
echo ""

exit $ERRORS

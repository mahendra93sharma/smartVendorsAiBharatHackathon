#!/bin/bash

# Script to generate a release keystore for Android app signing
# This should be run once to create the keystore file

set -e

echo "=========================================="
echo "Android Release Keystore Generator"
echo "=========================================="
echo ""
echo "This script will generate a release keystore for signing your Android app."
echo "IMPORTANT: Store the keystore file and passwords securely!"
echo ""

# Default values
DEFAULT_KEYSTORE_FILE="release.keystore"
DEFAULT_KEY_ALIAS="vendor-app-key"
DEFAULT_VALIDITY="10000"

# Prompt for keystore file name
read -p "Keystore filename [$DEFAULT_KEYSTORE_FILE]: " KEYSTORE_FILE
KEYSTORE_FILE=${KEYSTORE_FILE:-$DEFAULT_KEYSTORE_FILE}

# Check if keystore already exists
if [ -f "$KEYSTORE_FILE" ]; then
    echo ""
    echo "ERROR: Keystore file '$KEYSTORE_FILE' already exists!"
    echo "Please choose a different name or delete the existing file."
    exit 1
fi

# Prompt for key alias
read -p "Key alias [$DEFAULT_KEY_ALIAS]: " KEY_ALIAS
KEY_ALIAS=${KEY_ALIAS:-$DEFAULT_KEY_ALIAS}

# Prompt for validity
read -p "Validity in days [$DEFAULT_VALIDITY]: " VALIDITY
VALIDITY=${VALIDITY:-$DEFAULT_VALIDITY}

echo ""
echo "Generating keystore with the following settings:"
echo "  Keystore file: $KEYSTORE_FILE"
echo "  Key alias: $KEY_ALIAS"
echo "  Validity: $VALIDITY days"
echo ""

# Generate the keystore
keytool -genkeypair -v \
  -storetype PKCS12 \
  -keystore "$KEYSTORE_FILE" \
  -alias "$KEY_ALIAS" \
  -keyalg RSA \
  -keysize 2048 \
  -validity "$VALIDITY"

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "Keystore generated successfully!"
    echo "=========================================="
    echo ""
    echo "IMPORTANT: Save these details securely:"
    echo "  Keystore file: $(pwd)/$KEYSTORE_FILE"
    echo "  Key alias: $KEY_ALIAS"
    echo ""
    echo "To use this keystore for release builds, set these environment variables:"
    echo ""
    echo "  export KEYSTORE_FILE=$(pwd)/$KEYSTORE_FILE"
    echo "  export KEYSTORE_PASSWORD=<your_keystore_password>"
    echo "  export KEY_ALIAS=$KEY_ALIAS"
    echo "  export KEY_PASSWORD=<your_key_password>"
    echo ""
    echo "Then build the release APK:"
    echo "  cd android"
    echo "  ./gradlew assembleRelease"
    echo ""
    echo "WARNING: Never commit the keystore file to version control!"
    echo "         It is already added to .gitignore"
    echo ""
else
    echo ""
    echo "ERROR: Failed to generate keystore"
    exit 1
fi

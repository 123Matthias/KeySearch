#!/bin/bash
# build_dmg.sh - MIT CREATE-DMG (schöneres Layout)

APP_NAME="FileSearch"
VERSION="v0.0.0-alpha"
DMG_NAME="${APP_NAME}-${VERSION}.dmg"

echo "📦 Erstelle DMG für $APP_NAME $VERSION mit create-dmg..."

# Prüfen ob create-dmg installiert ist
if ! command -v create-dmg &> /dev/null; then
    echo "❌ create-dmg nicht gefunden. Installiere mit: brew install create-dmg"
    exit 1
fi

# DMG mit create-dmg erstellen
create-dmg \
  --volname "$APP_NAME" \
  --volicon "assets/img/logo.icns" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "$APP_NAME.app" 200 190 \
  --hide-extension "$APP_NAME.app" \
  --app-drop-link 600 185 \
  "$DMG_NAME" \
  "dist/$APP_NAME.app"

echo "✅ Fertig: $DMG_NAME"
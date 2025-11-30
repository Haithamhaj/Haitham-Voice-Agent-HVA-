#!/bin/bash

# ═══════════════════════════════════════════════════════════
#  🎨 Create macOS App Bundles with Custom Icons
#  إنشاء تطبيقات macOS بأيقونات مخصصة
# ═══════════════════════════════════════════════════════════

PROJECT_DIR="/Users/haitham/development/Haitham Voice Agent (HVA)"
ICONS_DIR="$PROJECT_DIR/icons"
APPS_DIR="$PROJECT_DIR/apps"

echo "🎨 إنشاء تطبيقات macOS بأيقونات مخصصة..."
echo ""

# Create apps directory
mkdir -p "$APPS_DIR"

# Function to create app bundle
create_app() {
    local app_name="$1"
    local icon_file="$2"
    local script_command="$3"
    local display_name="$4"
    
    echo "📦 إنشاء: $app_name.app"
    
    local app_path="$APPS_DIR/$app_name.app"
    
    # Remove existing app
    rm -rf "$app_path"
    
    # Create app bundle structure
    mkdir -p "$app_path/Contents/MacOS"
    mkdir -p "$app_path/Contents/Resources"
    
    # Copy icon
    cp "$icon_file" "$app_path/Contents/Resources/AppIcon.icns"
    
    # Create executable script
    cat > "$app_path/Contents/MacOS/$app_name" <<EOF
#!/bin/bash
cd "$PROJECT_DIR"
$script_command
EOF
    
    chmod +x "$app_path/Contents/MacOS/$app_name"
    
    # Create Info.plist
    cat > "$app_path/Contents/Info.plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>$app_name</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundleIdentifier</key>
    <string>com.haitham.hva.$app_name</string>
    <key>CFBundleName</key>
    <string>$display_name</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF
    
    echo "  ✅ تم إنشاء: $app_name.app"
    echo ""
}

# Create apps
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

create_app "HVA-Simple" \
    "$ICONS_DIR/microphone.icns" \
    'source .venv/bin/activate && python -m haitham_voice_agent.hva_menubar' \
    "🎤 HVA Simple"

create_app "HVA-Start" \
    "$ICONS_DIR/robot.icns" \
    'osascript -e "tell application \"Terminal\" to do script \"cd \\\"$PROJECT_DIR\\\" && source .venv/bin/activate && python -m haitham_voice_agent.main\""' \
    "🤖 Start HVA"

create_app "HVA-Dashboard" \
    "$ICONS_DIR/dashboard.icns" \
    'open "dashboard/index.html"' \
    "📊 HVA Dashboard"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ تم إنشاء جميع التطبيقات!"
echo ""
echo "📁 الموقع: $APPS_DIR"
echo ""
echo "📋 التطبيقات المنشأة:"
echo "  • HVA-Simple.app     - الوكيل الصوتي المبسط 🎤"
echo "  • HVA-Start.app      - الوكيل الصوتي الكامل 🤖"
echo "  • HVA-Dashboard.app  - لوحة الخدمات 📊"
echo ""
echo "💡 لنسخها لسطح المكتب:"
echo "   cp -r \"$APPS_DIR\"/*.app ~/Desktop/"
echo ""

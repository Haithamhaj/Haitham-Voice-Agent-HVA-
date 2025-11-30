#!/bin/bash

# ═══════════════════════════════════════════════════════════
#  🎨 Apply Custom Icons to HVA Files
#  تطبيق الأيقونات المخصصة على ملفات HVA
# ═══════════════════════════════════════════════════════════

PROJECT_DIR="/Users/haitham/development/Haitham Voice Agent (HVA)"
ICONS_DIR="$PROJECT_DIR/icons"

echo "🎨 تطبيق الأيقونات المخصصة..."
echo ""

# Function to apply icon to file
apply_icon() {
    local icon_file="$1"
    local target_file="$2"
    local name="$3"
    
    if [ ! -f "$icon_file" ]; then
        echo "⚠️  الأيقونة غير موجودة: $icon_file"
        return 1
    fi
    
    if [ ! -f "$target_file" ]; then
        echo "⚠️  الملف غير موجود: $target_file"
        return 1
    fi
    
    echo "📌 تطبيق أيقونة $name..."
    
    # Convert PNG to ICNS using sips and iconutil
    local temp_iconset="${icon_file%.png}.iconset"
    mkdir -p "$temp_iconset"
    
    # Create different sizes for iconset
    sips -z 16 16     "$icon_file" --out "${temp_iconset}/icon_16x16.png" > /dev/null 2>&1
    sips -z 32 32     "$icon_file" --out "${temp_iconset}/icon_16x16@2x.png" > /dev/null 2>&1
    sips -z 32 32     "$icon_file" --out "${temp_iconset}/icon_32x32.png" > /dev/null 2>&1
    sips -z 64 64     "$icon_file" --out "${temp_iconset}/icon_32x32@2x.png" > /dev/null 2>&1
    sips -z 128 128   "$icon_file" --out "${temp_iconset}/icon_128x128.png" > /dev/null 2>&1
    sips -z 256 256   "$icon_file" --out "${temp_iconset}/icon_128x128@2x.png" > /dev/null 2>&1
    sips -z 256 256   "$icon_file" --out "${temp_iconset}/icon_256x256.png" > /dev/null 2>&1
    sips -z 512 512   "$icon_file" --out "${temp_iconset}/icon_256x256@2x.png" > /dev/null 2>&1
    sips -z 512 512   "$icon_file" --out "${temp_iconset}/icon_512x512.png" > /dev/null 2>&1
    cp "$icon_file" "${temp_iconset}/icon_512x512@2x.png"
    
    # Convert iconset to icns
    local icns_file="${icon_file%.png}.icns"
    iconutil -c icns "$temp_iconset" -o "$icns_file" > /dev/null 2>&1
    
    # Clean up iconset
    rm -rf "$temp_iconset"
    
    # Apply icon using AppleScript
    osascript > /dev/null 2>&1 <<EOF
use framework "Foundation"
use framework "AppKit"

set sourcePath to "$icns_file"
set destPath to "$target_file"

set imageData to (current application's NSImage's alloc()'s initWithContentsOfFile:sourcePath)
(current application's NSWorkspace's sharedWorkspace()'s setIcon:imageData forFile:destPath options:2)
EOF
    
    if [ $? -eq 0 ]; then
        echo "  ✅ تم تطبيق الأيقونة على: $(basename "$target_file")"
    else
        echo "  ❌ فشل تطبيق الأيقونة على: $(basename "$target_file")"
    fi
    
    echo ""
}

# Apply icons to files
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Microphone icon for HVA Simple
apply_icon "$ICONS_DIR/microphone.png" "$PROJECT_DIR/HVA Simple.command" "المايك"
apply_icon "$ICONS_DIR/microphone.png" ~/Desktop/"HVA Simple.command" "المايك (سطح المكتب)"

# Robot icon for Start HVA
apply_icon "$ICONS_DIR/robot.png" "$PROJECT_DIR/Start HVA.command" "الروبوت"
apply_icon "$ICONS_DIR/robot.png" ~/Desktop/"Start HVA.command" "الروبوت (سطح المكتب)"

# Dashboard icon for Open Dashboard
apply_icon "$ICONS_DIR/dashboard.png" "$PROJECT_DIR/dashboard/Open Dashboard.command" "اللوحة"
apply_icon "$ICONS_DIR/dashboard.png" ~/Desktop/"Open Dashboard.command" "اللوحة (سطح المكتب)"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ تم تطبيق جميع الأيقونات بنجاح!"
echo ""
echo "💡 ملاحظة: قد تحتاج إلى:"
echo "   1. إعادة تشغيل Finder: killall Finder"
echo "   2. أو تحريك الملفات قليلاً لتحديث العرض"
echo ""

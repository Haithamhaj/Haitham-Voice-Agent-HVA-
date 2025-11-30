#!/bin/bash

# Convert PNG icons to ICNS format

PROJECT_DIR="/Users/haitham/development/Haitham Voice Agent (HVA)"
ICONS_DIR="$PROJECT_DIR/icons"

cd "$ICONS_DIR"

echo "🎨 تحويل الأيقونات إلى تنسيق ICNS..."
echo ""

convert_to_icns() {
    local png_file="$1"
    local base_name="${png_file%.png}"
    
    echo "📌 تحويل: $png_file"
    
    # Create iconset directory
    local iconset="${base_name}.iconset"
    mkdir -p "$iconset"
    
    # Generate all required sizes
    sips -z 16 16     "$png_file" --out "${iconset}/icon_16x16.png" 2>/dev/null
    sips -z 32 32     "$png_file" --out "${iconset}/icon_16x16@2x.png" 2>/dev/null
    sips -z 32 32     "$png_file" --out "${iconset}/icon_32x32.png" 2>/dev/null
    sips -z 64 64     "$png_file" --out "${iconset}/icon_32x32@2x.png" 2>/dev/null
    sips -z 128 128   "$png_file" --out "${iconset}/icon_128x128.png" 2>/dev/null
    sips -z 256 256   "$png_file" --out "${iconset}/icon_128x128@2x.png" 2>/dev/null
    sips -z 256 256   "$png_file" --out "${iconset}/icon_256x256.png" 2>/dev/null
    sips -z 512 512   "$png_file" --out "${iconset}/icon_256x256@2x.png" 2>/dev/null
    sips -z 512 512   "$png_file" --out "${iconset}/icon_512x512.png" 2>/dev/null
    cp "$png_file" "${iconset}/icon_512x512@2x.png"
    
    # Convert to icns
    iconutil -c icns "$iconset" -o "${base_name}.icns" 2>/dev/null
    
    # Clean up
    rm -rf "$iconset"
    
    if [ -f "${base_name}.icns" ]; then
        echo "  ✅ تم: ${base_name}.icns"
    else
        echo "  ❌ فشل: ${base_name}.icns"
    fi
    echo ""
}

# Convert all PNG files
for png in *.png; do
    if [ -f "$png" ]; then
        convert_to_icns "$png"
    fi
done

echo "✅ تم تحويل جميع الأيقونات!"
ls -lh *.icns 2>/dev/null

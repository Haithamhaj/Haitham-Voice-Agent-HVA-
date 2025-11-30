#!/bin/zsh

# ═══════════════════════════════════════════════════════════
#  🎤 Haitham Voice Agent - Launcher
#  تشغيل الوكيل الصوتي الذكي
# ═══════════════════════════════════════════════════════════

PROJECT_DIR="/Users/haitham/development/Haitham Voice Agent (HVA)"
VENV_PYTHON="$PROJECT_DIR/.venv/bin/python"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  🎤 Haitham Voice Agent"
echo "  وكيلك الصوتي الذكي"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check if HVA is already running
if pgrep -f "haitham_voice_agent.main" > /dev/null 2>&1; then
  echo "${RED}🔴 HVA يعمل حالياً${NC}"
  echo "${YELLOW}⏹️  إيقاف النظام...${NC}"
  pkill -f "haitham_voice_agent.main"
  sleep 1
  echo "${GREEN}✅ تم إيقاف HVA بنجاح${NC}"
  echo ""
  echo "اضغط أي مفتاح للإغلاق..."
  read -n 1
  exit 0
fi

# Start HVA
echo "${GREEN}🟢 بدء تشغيل HVA...${NC}"
echo ""

cd "$PROJECT_DIR"

# Check if virtual environment exists
if [ ! -f "$VENV_PYTHON" ]; then
  echo "${RED}⚠️  البيئة الافتراضية غير موجودة!${NC}"
  echo "${YELLOW}📦 إنشاء البيئة الافتراضية...${NC}"
  python3 -m venv .venv
  echo "${GREEN}✅ تم إنشاء البيئة الافتراضية${NC}"
  echo ""
  echo "${YELLOW}📥 تثبيت المتطلبات...${NC}"
  "$VENV_PYTHON" -m pip install --upgrade pip
  "$VENV_PYTHON" -m pip install -r requirements.txt
  echo "${GREEN}✅ تم تثبيت المتطلبات${NC}"
  echo ""
fi

# Check .env file
if [ ! -f "$PROJECT_DIR/.env" ]; then
  echo "${RED}⚠️  ملف .env غير موجود!${NC}"
  echo "${YELLOW}📝 يرجى إنشاء ملف .env مع المفاتيح المطلوبة${NC}"
  echo ""
  echo "مثال:"
  echo "  OPENAI_API_KEY=sk-..."
  echo "  GEMINI_API_KEY=AIza..."
  echo ""
  echo "اضغط أي مفتاح للإغلاق..."
  read -n 1
  exit 1
fi

# Display startup info
echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "${GREEN}✨ النظام جاهز للعمل!${NC}"
echo ""
echo "📋 الأوامر المتاحة:"
echo "  • احفظ ملاحظة: [محتوى الملاحظة]"
echo "  • ابحث في الملاحظات عن [موضوع]"
echo "  • اقرأ آخر إيميل"
echo "  • لخص آخر 5 إيميلات"
echo "  • اعرض الملفات في [مجلد]"
echo "  • افتح تطبيق [اسم التطبيق]"
echo ""
echo "🎤 تحدث بوضوح بالعربية أو الإنجليزية"
echo "🛑 للإيقاف: Ctrl+C أو شغّل هذا الملف مرة أخرى"
echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Run HVA
"$VENV_PYTHON" -m haitham_voice_agent.main

# If HVA exits
echo ""
echo "${YELLOW}⏹️  تم إيقاف HVA${NC}"
echo ""

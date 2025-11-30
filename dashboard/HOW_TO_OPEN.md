# 🚀 طرق فتح لوحة خدمات HVA

## الطريقة 1️⃣: النقر المزدوج (الأسهل) ⭐

**على سطح المكتب:**
- ابحث عن ملف `Open Dashboard.command` على سطح المكتب
- انقر عليه نقرتين لفتح اللوحة

**في مجلد المشروع:**
```
/Users/haitham/development/Haitham Voice Agent (HVA)/dashboard/Open Dashboard.command
```

## الطريقة 2️⃣: من Terminal

```bash
# الطريقة السريعة
cd "/Users/haitham/development/Haitham Voice Agent (HVA)"
./dashboard/open_dashboard.sh

# أو مباشرة
open "/Users/haitham/development/Haitham Voice Agent (HVA)/dashboard/index.html"
```

## الطريقة 3️⃣: إضافة Bookmark في المتصفح

1. افتح اللوحة في المتصفح
2. اضغط `⌘ + D` لحفظ Bookmark
3. في المرات القادمة، افتح من Bookmarks

## الطريقة 4️⃣: إنشاء Alias في Terminal

أضف هذا السطر إلى ملف `~/.zshrc`:

```bash
alias hva-dashboard='open "/Users/haitham/development/Haitham Voice Agent (HVA)/dashboard/index.html"'
```

ثم في أي وقت، اكتب في Terminal:
```bash
hva-dashboard
```

## الطريقة 5️⃣: من Finder

1. افتح Finder
2. اذهب إلى:
   ```
   /Users/haitham/development/Haitham Voice Agent (HVA)/dashboard/
   ```
3. انقر نقرتين على `index.html`

## الطريقة 6️⃣: إضافة إلى Dock

1. افتح مجلد `dashboard`
2. اسحب ملف `Open Dashboard.command` إلى Dock
3. انقر عليه في أي وقت لفتح اللوحة

---

## 🎯 الطريقة الموصى بها

**للاستخدام اليومي:** استخدم ملف `Open Dashboard.command` على سطح المكتب - فقط انقر نقرتين! ✨

**للمطورين:** استخدم الـ alias في Terminal لفتح سريع من أي مكان 🚀

# نظام Provider Dashboard - Frontend

React (Vite) + Tailwind CSS، RTL بالكامل، مبني بالظبط على تصميم
شاشة الداشبورد اللي معايا. متصل مباشرة بالـ Backend.

## التشغيل

```bash
npm install
npm run dev
```

هيفتح على `http://localhost:5173`. الـ dev server معمول عليه proxy
تلقائي لأي request على `/provider/*` و `/public/*` لـ
`http://localhost:8000` (الباك اند)، يعني لازم تشغّل الباك اند على
بورت 8000 قبل ما تفتح الفرونت.

لو الباك اند شغال على بورت أو domain مختلف، عدّل `vite.config.js`
أو استخدم `VITE_API_URL` في ملف `.env`.

## البناء للنشر

```bash
npm run build
```

الناتج هيبقى في `dist/` - أي static host (Vercel, Netlify, أو حتى
FastAPI نفسه بـ StaticFiles) يقدر يسيبه.

## الصفحات

- `/login`, `/register` - تسجيل الدخول وإنشاء حساب مزود جديد
- `/dashboard` - الشاشة الرئيسية (KPIs، خدمات، حجوزات، تقييمات، توثيق)
- `/bookings` - كل الحجوزات مع فلترة وتحديث حالة
- `/services` - إدارة الخدمات (إضافة/تعديل/حذف/تفعيل)
- `/analytics` - رسم بياني للإيرادات + أفضل الخدمات
- `/support` - تذاكر الدعم الفني

## نظام التصميم

الألوان والخطوط متعرفة كـ CSS variables في `src/index.css`
(`--color-gold`, `--color-nile`, `--color-coral`, `--color-sand`،
Cairo للعناوين، IBM Plex Sans Arabic للنصوص) - نفس نظام رِحلة
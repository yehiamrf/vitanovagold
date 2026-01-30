# VitaNova Authentication System

## نظام المصادقة - VitaNova

هذا النظام يوفر مصادقة كاملة لمنصة VitaNova للذهب، مع دعم كامل للعربية.

---

## المميزات

- ✅ **تسجيل المستخدمين** (إنشاء حساب) مع التحقق من صحة البيانات
- ✅ **تسجيل الدخول** مع خيار "تذكرني"
- ✅ **تشفير كلمات المرور** باستخدام Bcrypt
- ✅ **hCaptcha** للحماية من الروبوتات
- ✅ **التحقق من البريد الإلكتروني** عبر روابط مؤقتة
- ✅ **استعادة كلمة المرور** عبر رابط آمن
- ✅ **تسجيل البريد الإلكتروني في CSV** للإرسال لاحقاً
- ✅ **حماية من هجمات القوة الغاشمة** (قفل الحساب بعد محاولات فاشلة)
- ✅ **واجهة عربية كاملة** مع RTL

---

## التثبيت

### 1. تثبيت المتطلبات

```bash
cd backend
pip install -r requirements.txt
```

أو يدوياً:

```bash
pip install flask flask-cors flask-bcrypt flask-login flask-sqlalchemy flask-wtf itsdangerous requests
```

### 2. إعداد hCaptcha (اختياري للتطوير)

1. سجل في [hCaptcha.com](https://www.hcaptcha.com/)
2. احصل على Site Key و Secret Key
3. حدّث الملف `config.py`:

```python
HCAPTCHA_SITE_KEY = 'your-site-key'
HCAPTCHA_SECRET_KEY = 'your-secret-key'
```

> **ملاحظة**: المفاتيح الافتراضية هي مفاتيح اختبار تقبل أي إدخال.

### 3. تشغيل الخادم

```bash
cd backend
python Goldprices.py
```

الخادم سيعمل على: `http://127.0.0.1:5000`

---

## هيكل الملفات

```
backend/
├── Goldprices.py          # الخادم الرئيسي (Gold API + Auth)
├── config.py              # إعدادات المصادقة
├── models.py              # نماذج قاعدة البيانات (User, LoginLog)
├── auth_routes.py         # مسارات API للمصادقة
├── tokens.py              # إنشاء والتحقق من الرموز
├── validators.py          # التحقق من صحة البيانات
├── email_logger.py        # تسجيل البريد في CSV
├── captcha.py             # التحقق من hCaptcha
├── requirements.txt       # المتطلبات
├── vitanova.db            # قاعدة البيانات (تُنشأ تلقائياً)
├── emails_pending_verification.csv  # سجل التحقق
└── password_reset_requests.csv      # سجل استعادة كلمة المرور

frontend/
├── login.html             # صفحة تسجيل الدخول
├── register.html          # صفحة إنشاء الحساب
├── forgot-password.html   # صفحة نسيت كلمة المرور
├── reset-password.html    # صفحة إعادة تعيين كلمة المرور
├── verify-email.html      # صفحة التحقق من البريد
└── store.html             # المتجر (محدّث مع Auth UI)
```

---

## نقاط API

### التسجيل
```
POST /auth/register
{
    "username": "أحمد",
    "email": "ahmed@example.com",
    "password": "SecurePass123",
    "confirm_password": "SecurePass123",
    "full_name": "أحمد محمد",      // اختياري
    "phone": "+971501234567",       // اختياري
    "h-captcha-response": "token"
}
```

### تسجيل الدخول
```
POST /auth/login
{
    "username": "أحمد",            // أو email
    "password": "SecurePass123",
    "remember_me": true,
    "h-captcha-response": "token"
}
```

### تسجيل الخروج
```
POST /auth/logout
```

### التحقق من حالة المصادقة
```
GET /auth/check
```

### المستخدم الحالي
```
GET /auth/me
```

### التحقق من البريد الإلكتروني
```
GET/POST /auth/verify-email/<token>
```

### إعادة إرسال رابط التحقق
```
POST /auth/resend-verification
{
    "email": "ahmed@example.com"
}
```

### نسيت كلمة المرور
```
POST /auth/forgot-password
{
    "email": "ahmed@example.com",
    "h-captcha-response": "token"
}
```

### إعادة تعيين كلمة المرور
```
POST /auth/reset-password/<token>
{
    "password": "NewSecurePass123",
    "confirm_password": "NewSecurePass123"
}
```

### تغيير كلمة المرور (مسجل الدخول)
```
POST /auth/change-password
{
    "current_password": "OldPass123",
    "new_password": "NewSecurePass456",
    "confirm_password": "NewSecurePass456"
}
```

### فحص قوة كلمة المرور
```
POST /auth/password-strength
{
    "password": "TestPassword123"
}
```

---

## متطلبات كلمة المرور

- 8 أحرف على الأقل
- حرف كبير واحد على الأقل (A-Z)
- حرف صغير واحد على الأقل (a-z)
- رقم واحد على الأقل (0-9)

---

## الأمان

### تشفير كلمة المرور
- يستخدم **Bcrypt** مع 12 جولة (rounds)
- تضاف salt تلقائياً
- مقارنة بوقت ثابت (constant-time comparison)

### حماية الجلسة
- ملفات تعريف الارتباط (cookies) آمنة
- حماية الجلسة من التزوير (CSRF)
- وضع "strong" للتحقق من IP/User Agent

### حماية من القوة الغاشمة
- 5 محاولات فاشلة = قفل 15 دقيقة
- تسجيل جميع محاولات الدخول

### الرموز
- رموز موقعة (signed tokens) باستخدام itsdangerous
- انتهاء الصلاحية:
  - التحقق من البريد: ساعة واحدة
  - استعادة كلمة المرور: 30 دقيقة
  - تذكرني: 30 يوم

---

## الاختبار

### اختبار التسجيل
1. افتح `frontend/register.html`
2. املأ النموذج
3. اضغط "إنشاء الحساب"
4. انظر console للـ verification token

### اختبار تسجيل الدخول
1. افتح `frontend/login.html`
2. أدخل بيانات المستخدم
3. اضغط "تسجيل الدخول"

### اختبار التحقق من البريد
```
http://localhost:5500/verify-email.html?token=YOUR_TOKEN
```

### اختبار استعادة كلمة المرور
1. افتح `frontend/forgot-password.html`
2. أدخل البريد الإلكتروني
3. انظر console للـ reset token
4. افتح: `reset-password.html?token=YOUR_TOKEN`

---

## ملاحظات للإنتاج

1. **غيّر SECRET_KEY** في `config.py` إلى قيمة عشوائية آمنة
2. **فعّل HTTPS** واضبط `SESSION_COOKIE_SECURE = True`
3. **استخدم مفاتيح hCaptcha** حقيقية
4. **أرسل الإيميلات فعلياً** بدلاً من تسجيلها في CSV
5. **استخدم قاعدة بيانات** أقوى (PostgreSQL/MySQL) للإنتاج

---

## الترخيص

هذا المشروع مخصص لـ VitaNova MVP.

/**
 * VitaNova Multi-Language Support Module
 * Handles Arabic/English translation and RTL/LTR switching
 */

const VitaNovaLang = (function() {
  'use strict';

  // ========== TRANSLATION DATA ==========
  const translations = {
    ar: {
      // Brand
      brandTagline: "سبائك ذهب عيار 24",
      
      // Navigation
      navHome: "الرئيسية",
      navStore: "المتجر",
      navNews: "الأخبار",
      navAbout: "من نحن",
      navContact: "اتصل بنا",
      
      // Auth
      login: "تسجيل الدخول",
      register: "إنشاء حساب",
      myAccount: "حسابي",
      orderHistory: "سجل الطلبات",
      logout: "تسجيل الخروج",
      
      // Footer
      footerAbout: "منصة موثوقة لبيع سبائك الذهب عيار 24 داخل الإمارات. نقدم أسعارًا شفافة وتسليمًا سريعًا مع ضمان الجودة.",
      footerQuickLinks: "روابط سريعة",
      footerLegal: "معلومات قانونية",
      footerFaq: "الأسئلة الشائعة",
      footerPrivacy: "سياسة الخصوصية",
      footerTerms: "الشروط والأحكام",
      footerCopyright: "© 2025 Vita Nova. جميع الحقوق محفوظة.",
      footerAdmin: "⚙️ لوحة الإدارة",
      
      // Home Page
      homeTitle: "مرحباً بك في Vita Nova",
      homeSubtitle: "منصتك الموثوقة لشراء سبائك الذهب عيار 24 داخل الإمارات",
      
      // Store Page - Price Ticker
      currentPrice: "السعر الحالي للجرام — AED",
      withVat: "مع ضريبة 5%",
      commission: "العمولة",
      commissionByType: "حسب النوع",
      todayHigh: "أعلى سعر اليوم",
      todayLow: "أدنى سعر اليوم",
      lastUpdate: "آخر تحديث",
      refreshNow: "تحديث الآن",
      tickerNote: "💡 السعر يُعرض للشفافية. عند بدء الطلب يتم تثبيته 15 دقيقة لتجنب أي خلافات.",
      
      // Store Page - Chart
      priceHistory: "📈 تاريخ أسعار الذهب",
      timeframe1D: "يوم",
      timeframe1W: "أسبوع",
      timeframe1M: "شهر",
      timeframe6M: "6 أشهر",
      timeframe1Y: "سنة",
      timeframe5Y: "5 سنوات",
      timeframe15Y: "15 سنة",
      timeframeCustom: "تواريخ مخصصة",
      
      // Store Page - Products
      mvpSellOnly: "MVP — بيع فقط",
      chooseWeight: "اختر الوزن واطلب الآن",
      priceCalculation: "السعر النهائي = (سعر الذهب اللحظي × الوزن × ضريبة %5) + عمولة ثابتة.",
      priceLock: "تثبيت السعر",
      priceLockValue: "15 دقيقة",
      delivery: "التسليم",
      deliveryValue: "24–72 ساعة",
      payment: "الدفع",
      paymentValue: "أونلاين / COD",
      goldBar24k: "ذهب عيار 24 مختومة. السعر النهائي محسوب شفافًا حسب سعر اليوم زائد ضريبة %5 + ",
      fixedCommission: "عمولة ثابتة",
      percentCommission: "نسبة ثابتة",
      currentPriceBeforeVat: "السعر الحالي قبل الضريبة",
      addToCart: "أضف للسلة",
      
      // Store Page - Trust Note
      trustNote: "ملاحظة ثقة:",
      trustNoteText: "يتم تنفيذ تجهيز وتسليم الطلبات عبر شركاء متخصصين ومرخّصين داخل الإمارات وفق نظام White-label، مع فاتورة رسمية عند التسليم وسياسة استرجاع في حال عدم التسليم خلال المدة المحددة.",
      
      // Store Page - How it Works
      howItWorks: "كيف يعمل الطلب؟",
      howItWorksSubtitle: "تجربة بسيطة بدون تعقيد: طلب → تثبيت سعر → دفع → تسليم.",
      step1: "تختار الوزن وتضغط \"أضف للسلة\".",
      step2: "نثبّت السعر لمدة <b>15 دقيقة</b> لإتمام الطلب.",
      step3: "تختار طريقة الدفع: <b>أونلاين</b> أو <b>عند الاستلام</b>.",
      step4: "التجهيز والتسليم خلال <b>24–72 ساعة</b> داخل الإمارات.",
      pricingPolicy: "سياسة التسعير:",
      pricingPolicyText: "السعر يُحسب حسب سعر الذهب في وقت الطلب + عمولة تجهيز وتسليم ثابتة. لا توجد رسوم مخفية.",
      refundPolicy: "سياسة الاسترجاع:",
      refundPolicyText: "في حال عدم التسليم خلال 24–72 ساعة، يحق للعميل استرجاع المبلغ كاملًا.",
      disclaimer: "هذه صفحة تجريبية (MVP). لا تُعد نصيحة مالية ولا تمثل استثمارًا. بيع وتسليم ذهب فعلي فقط.",
      
      // Cart
      cart: "سلة التسوق",
      emptyCart: "السلة فارغة",
      product: "المنتج",
      quantity: "الكمية",
      total: "المجموع",
      includesVat: "يشمل ضريبة",
      includesCommission: "يشمل عمولة ثابتة",
      checkout: "إتمام الطلب",
      
      // Checkout Modal
      checkoutTitle: "إتمام الطلب",
      priceLocked15Min: "السعر مثبت لمدة 15 دقيقة لإتمام الطلب.",
      lockExpires: "سينتهي التثبيت عند انتهاء العدّاد.",
      timeRemaining: "الوقت المتبقي",
      orderDetails: "تفاصيل الطلب",
      productsInCart: "المنتجات في السلة",
      lockedGramPrice: "سعر الجرام المثبّت (AED)",
      totalWeight: "الوزن الإجمالي",
      totalVat: "الضريبة الإجمالية (AED)",
      totalCommission: "العمولة الإجمالية (AED)",
      finalPrice: "السعر النهائي (AED)",
      finalPriceFormula: "السعر النهائي = (سعر الجرام × الوزن الكلي × ضريبة 5%) + العمولة الثابتة.",
      customerInfo: "بيانات العميل وطريقة الدفع",
      name: "الاسم",
      phone: "الهاتف (واتساب)",
      emirate: "الإمارة",
      city: "المدينة",
      cityPlaceholder: "مثال: الخليج التجاري، مارينا",
      paymentMethod: "طريقة الدفع",
      payOnline: "الدفع أونلاين",
      payCod: "الدفع عند الاستلام",
      shortAddress: "العنوان المختصر",
      addressPlaceholder: "اكتب المنطقة/الشارع/ملاحظات التوصيل",
      sendToDealer: "إرسال الطلب للتاجر واتساب",
      copySummary: "نسخ ملخص الطلب",
      mvpNote: "* في الـ MVP هذا الإرسال يفتح واتساب برسالة جاهزة للتاجر. لاحقًا يمكن أتمتته.",
      deliveryPolicy: "سياسة التسليم:",
      deliveryPolicyText: "التسليم خلال 24–72 ساعة داخل الإمارات. في حال عدم التسليم خلال المدة المحددة، يحق للعميل استرجاع المبلغ كاملًا.",
      
      // Emirates
      dubai: "دبي",
      abuDhabi: "أبوظبي",
      sharjah: "الشارقة",
      ajman: "عجمان",
      rasAlKhaimah: "رأس الخيمة",
      fujairah: "الفجيرة",
      ummAlQuwain: "أم القيوين",
      
      // Date Picker
      selectDateRange: "📅 اختر نطاق التواريخ",
      fromDate: "من تاريخ",
      toDate: "إلى تاريخ",
      apply: "تطبيق",
      cancel: "إلغاء",
      
      // Admin
      adminPanel: "لوحة التحكم",
      adminLogin: "تسجيل دخول الإدارة",
      username: "اسم المستخدم",
      password: "كلمة المرور",
      enter: "دخول",
      priceSettings: "إعدادات السعر",
      commissionSettings: "العمولة",
      close: "إغلاق",
      back: "أرجع",
      save: "حفظ",
      
      // Settings Modal
      priceMode: "وضع السعر اليدوي",
      goldPricePerGram: "سعر الذهب للجرام (AED)",
      manualModeNote: "هذا يكفي لتجربة الـ MVP بدون أي API.",
      saveManualPrice: "حفظ السعر اليدوي",
      useManualMode: "استخدم الوضع اليدوي",
      apiMode: "وضع API (اختياري)",
      apiSecurityWarning: "تنبيه أمني:",
      apiSecurityNote: "الأفضل أن يكون مفتاح الـ API في السيرفر. هذه صفحة MVP بدون سيرفر، فلو وضعت المفتاح هنا سيكون ظاهرًا لمن يفحص الكود. إذا كان هذا غير مناسب، استمر بالسعر اليدوي.",
      apiUrl: "رابط API (GET)",
      apiUrlNote: "يجب أن يرجع JSON يحتوي سعر الجرام بالدرهم.",
      jsonPath: "طريقة استخراج السعر من JSON",
      jsonPathNote: "اكتب المسار مثل:",
      enableApiMode: "تفعيل وضع API",
      testApi: "اختبار API",
      apiProviderNote: "يمكنك استخدام أي مزود سعر (Metals-API / GoldAPI / GoldPriceZ…). المهم أن يكون الناتج \"AED لكل جرام\".",
      result: "النتيجة:",
      resultNote: "تحديث لحظي كل 60 ثانية + تثبيت السعر 15 دقيقة عند بدء الطلب.",
      
      // Commission Modal
      commissionSettingsTitle: "إعدادات العمولة",
      commissionSettingsSubtitle: "اختر نوع العمولة وحدد قيمتها لكل منتج.",
      saveCommissionSettings: "حفظ إعدادات العمولة",
      commissionNote: "ملاحظة:",
      fixedCommissionNote: "العمولة الثابتة تُضاف مباشرة بالدرهم لكل نوع.",
      percentCommissionNote: "النسبة الثابتة تُحسب كنسبة مئوية من قيمة الذهب لكل نوع.",
      
      // About Page
      aboutTitle: "من نحن",
      aboutSubtitle: "تعرف على قصتنا ورؤيتنا في عالم الذهب",
      
      // Contact Page
      contactTitle: "اتصل بنا",
      contactSubtitle: "نحن هنا للإجابة على استفساراتك",
      
      // News Page
      newsTitle: "الأخبار",
      newsSubtitle: "آخر الأخبار والتحديثات من عالم الذهب",
      
      // FAQ Page
      faqTitle: "الأسئلة الشائعة",
      faqSubtitle: "إجابات على أكثر الأسئلة شيوعًا",
      
      // Privacy Page
      privacyTitle: "سياسة الخصوصية",
      privacySubtitle: "كيف نحمي بياناتك ونحترم خصوصيتك",
      
      // Terms Page
      termsTitle: "الشروط والأحكام",
      termsSubtitle: "اقرأ شروط وأحكام استخدام المنصة",
      
      // Account Page
      accountTitle: "حسابي",
      accountSubtitle: "إدارة معلومات حسابك",
      
      // Login Page
      loginTitle: "تسجيل الدخول",
      loginSubtitle: "أدخل بياناتك للوصول إلى حسابك",
      email: "البريد الإلكتروني",
      rememberMe: "تذكرني",
      forgotPassword: "نسيت كلمة المرور؟",
      noAccount: "ليس لديك حساب؟",
      createAccount: "أنشئ حساب جديد",
      
      // Register Page
      registerTitle: "إنشاء حساب جديد",
      registerSubtitle: "انضم إلينا وابدأ تجربة تسوق الذهب",
      confirmPassword: "تأكيد كلمة المرور",
      agreeToTerms: "أوافق على",
      termsAndConditions: "الشروط والأحكام",
      alreadyHaveAccount: "لديك حساب بالفعل؟",
      
      // Alerts & Messages
      alertEmptyCart: "السلة فارغة. من فضلك أضف منتجات للسلة أولاً.",
      alertSetPrice: "من فضلك ضع سعر الذهب أولًا من إعدادات السعر.",
      alertFillFields: "من فضلك اكتب الاسم، الهاتف، والعنوان.",
      alertPriceLockExpired: "انتهت مدة تثبيت السعر. سيتم إعادة احتساب السعر. من فضلك ابدأ الطلب مرة أخرى.",
      alertOrderSaved: "✅ تم حفظ الطلب بنجاح! رقم الطلب:",
      alertLoginRequired: "يجب تسجيل الدخول لحفظ الطلب. سيتم فتح واتساب فقط.",
      alertCopied: "تم نسخ ملخص الطلب.",
      alertCopyFailed: "لم يتم النسخ. انسخ يدويًا من صفحة الملخص.",
      alertInvalidPrice: "سعر غير صالح.",
      alertPriceSaved: "تم حفظ السعر اليدوي.",
      alertManualMode: "تم تفعيل الوضع اليدوي.",
      alertApiMode: "تم تفعيل وضع API. سيتم التحديث كل 60 ثانية.",
      alertApiTestSuccess: "نجح الاختبار. السعر المستخرج =",
      alertApiTestFailed: "فشل اختبار API. راجع الرابط أو مسار JSON.",
      alertEnterApiDetails: "من فضلك أدخل رابط API ومسار استخراج السعر.",
      alertCommissionSaved: "تم حفظ إعدادات العمولة بنجاح",
      alertWrongCredentials: "اسم المستخدم أو كلمة المرور غير صحيحة. حاول مرة أخرى.",
      alertSelectDates: "من فضلك اختر تاريخ البداية والنهاية",
      alertInvalidDateRange: "تاريخ البداية يجب أن يكون قبل تاريخ النهاية",
      
      // Misc
      loading: "جاري التحميل...",
      error: "حدث خطأ",
      perUnit: "للوحدة",
      aed: "AED",
      gram: "g",
      vatPercent: "ضريبة القيمة المضافة 5%",
    },
    
    en: {
      // Brand
      brandTagline: "24 Karat Gold Bullion",
      
      // Navigation
      navHome: "Home",
      navStore: "Store",
      navNews: "News",
      navAbout: "About Us",
      navContact: "Contact",
      
      // Auth
      login: "Login",
      register: "Register",
      myAccount: "My Account",
      orderHistory: "Order History",
      logout: "Logout",
      
      // Footer
      footerAbout: "A trusted platform for selling 24-karat gold bullion within the UAE. We offer transparent pricing and fast delivery with quality assurance.",
      footerQuickLinks: "Quick Links",
      footerLegal: "Legal Information",
      footerFaq: "FAQ",
      footerPrivacy: "Privacy Policy",
      footerTerms: "Terms & Conditions",
      footerCopyright: "© 2025 Vita Nova. All rights reserved.",
      footerAdmin: "⚙️ Admin Panel",
      
      // Home Page
      homeTitle: "Welcome to Vita Nova",
      homeSubtitle: "Your trusted platform for buying 24-karat gold bullion in the UAE",
      
      // Store Page - Price Ticker
      currentPrice: "Current Price per Gram — AED",
      withVat: "With 5% VAT",
      commission: "Commission",
      commissionByType: "By Type",
      todayHigh: "Today's High",
      todayLow: "Today's Low",
      lastUpdate: "Last Update",
      refreshNow: "Refresh Now",
      tickerNote: "💡 Price shown for transparency. When you start an order, it's locked for 15 minutes to avoid disputes.",
      
      // Store Page - Chart
      priceHistory: "📈 Gold Price History",
      timeframe1D: "Day",
      timeframe1W: "Week",
      timeframe1M: "Month",
      timeframe6M: "6 Months",
      timeframe1Y: "Year",
      timeframe5Y: "5 Years",
      timeframe15Y: "15 Years",
      timeframeCustom: "Custom Dates",
      
      // Store Page - Products
      mvpSellOnly: "MVP — Sell Only",
      chooseWeight: "Choose Weight and Order Now",
      priceCalculation: "Final price = (Live gold price × Weight × 5% VAT) + Fixed commission.",
      priceLock: "Price Lock",
      priceLockValue: "15 Minutes",
      delivery: "Delivery",
      deliveryValue: "24–72 Hours",
      payment: "Payment",
      paymentValue: "Online / COD",
      goldBar24k: "24K gold stamped bar. Final price calculated transparently based on today's price plus 5% VAT + ",
      fixedCommission: "Fixed Commission",
      percentCommission: "Percentage Commission",
      currentPriceBeforeVat: "Current Price Before VAT",
      addToCart: "Add to Cart",
      
      // Store Page - Trust Note
      trustNote: "Trust Note:",
      trustNoteText: "Order processing and delivery are handled by specialized and licensed partners within the UAE under a White-label system, with an official invoice upon delivery and a refund policy if delivery is not made within the specified period.",
      
      // Store Page - How it Works
      howItWorks: "How Does Ordering Work?",
      howItWorksSubtitle: "Simple experience without complications: Order → Lock Price → Pay → Deliver.",
      step1: "Choose weight and click \"Add to Cart\".",
      step2: "We lock the price for <b>15 minutes</b> to complete the order.",
      step3: "Choose payment method: <b>Online</b> or <b>Cash on Delivery</b>.",
      step4: "Processing and delivery within <b>24–72 hours</b> in the UAE.",
      pricingPolicy: "Pricing Policy:",
      pricingPolicyText: "Price calculated based on gold price at order time + fixed processing and delivery commission. No hidden fees.",
      refundPolicy: "Refund Policy:",
      refundPolicyText: "If delivery is not made within 24–72 hours, the customer is entitled to a full refund.",
      disclaimer: "This is a test page (MVP). Not financial advice and does not represent an investment. Physical gold sale and delivery only.",
      
      // Cart
      cart: "Shopping Cart",
      emptyCart: "Cart is empty",
      product: "Product",
      quantity: "Quantity",
      total: "Total",
      includesVat: "Includes VAT",
      includesCommission: "Includes fixed commission",
      checkout: "Checkout",
      
      // Checkout Modal
      checkoutTitle: "Complete Order",
      priceLocked15Min: "Price locked for 15 minutes to complete the order.",
      lockExpires: "Lock expires when the timer ends.",
      timeRemaining: "Time Remaining",
      orderDetails: "Order Details",
      productsInCart: "Products in Cart",
      lockedGramPrice: "Locked Price per Gram (AED)",
      totalWeight: "Total Weight",
      totalVat: "Total VAT (AED)",
      totalCommission: "Total Commission (AED)",
      finalPrice: "Final Price (AED)",
      finalPriceFormula: "Final price = (Price per gram × Total weight × 5% VAT) + Fixed commission.",
      customerInfo: "Customer Info & Payment Method",
      name: "Name",
      phone: "Phone (WhatsApp)",
      emirate: "Emirate",
      city: "City",
      cityPlaceholder: "e.g., Business Bay, Marina",
      paymentMethod: "Payment Method",
      payOnline: "Pay Online",
      payCod: "Cash on Delivery",
      shortAddress: "Short Address",
      addressPlaceholder: "Enter area/street/delivery notes",
      sendToDealer: "Send Order to Dealer via WhatsApp",
      copySummary: "Copy Order Summary",
      mvpNote: "* In the MVP, this sends a ready message to the dealer via WhatsApp. Can be automated later.",
      deliveryPolicy: "Delivery Policy:",
      deliveryPolicyText: "Delivery within 24–72 hours in the UAE. If delivery is not made within the specified period, the customer is entitled to a full refund.",
      
      // Emirates
      dubai: "Dubai",
      abuDhabi: "Abu Dhabi",
      sharjah: "Sharjah",
      ajman: "Ajman",
      rasAlKhaimah: "Ras Al Khaimah",
      fujairah: "Fujairah",
      ummAlQuwain: "Umm Al Quwain",
      
      // Date Picker
      selectDateRange: "📅 Select Date Range",
      fromDate: "From Date",
      toDate: "To Date",
      apply: "Apply",
      cancel: "Cancel",
      
      // Admin
      adminPanel: "Control Panel",
      adminLogin: "Admin Login",
      username: "Username",
      password: "Password",
      enter: "Enter",
      priceSettings: "Price Settings",
      commissionSettings: "Commission",
      close: "Close",
      back: "Back",
      save: "Save",
      
      // Settings Modal
      priceMode: "Manual Price Mode",
      goldPricePerGram: "Gold Price per Gram (AED)",
      manualModeNote: "This is sufficient to test the MVP without any API.",
      saveManualPrice: "Save Manual Price",
      useManualMode: "Use Manual Mode",
      apiMode: "API Mode (Optional)",
      apiSecurityWarning: "Security Warning:",
      apiSecurityNote: "It's best to keep the API key on the server. This is an MVP page without a server, so if you put the key here it will be visible to anyone who inspects the code. If this is not suitable, continue with manual pricing.",
      apiUrl: "API URL (GET)",
      apiUrlNote: "Must return JSON containing the gram price in AED.",
      jsonPath: "How to Extract Price from JSON",
      jsonPathNote: "Write the path like:",
      enableApiMode: "Enable API Mode",
      testApi: "Test API",
      apiProviderNote: "You can use any price provider (Metals-API / GoldAPI / GoldPriceZ…). The important thing is that the output is \"AED per gram\".",
      result: "Result:",
      resultNote: "Live update every 60 seconds + 15-minute price lock when starting an order.",
      
      // Commission Modal
      commissionSettingsTitle: "Commission Settings",
      commissionSettingsSubtitle: "Choose commission type and set its value for each product.",
      saveCommissionSettings: "Save Commission Settings",
      commissionNote: "Note:",
      fixedCommissionNote: "Fixed commission is added directly in AED for each type.",
      percentCommissionNote: "Percentage commission is calculated as a percentage of gold value for each type.",
      
      // About Page
      aboutTitle: "About Us",
      aboutSubtitle: "Learn about our story and vision in the world of gold",
      
      // Contact Page
      contactTitle: "Contact Us",
      contactSubtitle: "We're here to answer your questions",
      
      // News Page
      newsTitle: "News",
      newsSubtitle: "Latest news and updates from the world of gold",
      
      // FAQ Page
      faqTitle: "Frequently Asked Questions",
      faqSubtitle: "Answers to the most common questions",
      
      // Privacy Page
      privacyTitle: "Privacy Policy",
      privacySubtitle: "How we protect your data and respect your privacy",
      
      // Terms Page
      termsTitle: "Terms & Conditions",
      termsSubtitle: "Read the platform's terms of use",
      
      // Account Page
      accountTitle: "My Account",
      accountSubtitle: "Manage your account information",
      
      // Login Page
      loginTitle: "Login",
      loginSubtitle: "Enter your details to access your account",
      email: "Email",
      rememberMe: "Remember Me",
      forgotPassword: "Forgot Password?",
      noAccount: "Don't have an account?",
      createAccount: "Create New Account",
      
      // Register Page
      registerTitle: "Create New Account",
      registerSubtitle: "Join us and start your gold shopping experience",
      confirmPassword: "Confirm Password",
      agreeToTerms: "I agree to the",
      termsAndConditions: "Terms & Conditions",
      alreadyHaveAccount: "Already have an account?",
      
      // Alerts & Messages
      alertEmptyCart: "Cart is empty. Please add products to cart first.",
      alertSetPrice: "Please set the gold price first from price settings.",
      alertFillFields: "Please enter name, phone, and address.",
      alertPriceLockExpired: "Price lock has expired. Price will be recalculated. Please start the order again.",
      alertOrderSaved: "✅ Order saved successfully! Order ID:",
      alertLoginRequired: "Login required to save order. Only WhatsApp will open.",
      alertCopied: "Order summary copied.",
      alertCopyFailed: "Copy failed. Please copy manually from the summary page.",
      alertInvalidPrice: "Invalid price.",
      alertPriceSaved: "Manual price saved.",
      alertManualMode: "Manual mode activated.",
      alertApiMode: "API mode activated. Will update every 60 seconds.",
      alertApiTestSuccess: "Test successful. Extracted price =",
      alertApiTestFailed: "API test failed. Check the URL or JSON path.",
      alertEnterApiDetails: "Please enter API URL and price extraction path.",
      alertCommissionSaved: "Commission settings saved successfully",
      alertWrongCredentials: "Username or password is incorrect. Try again.",
      alertSelectDates: "Please select start and end dates",
      alertInvalidDateRange: "Start date must be before end date",
      
      // Misc
      loading: "Loading...",
      error: "An error occurred",
      perUnit: "per unit",
      aed: "AED",
      gram: "g",
      vatPercent: "5% VAT",
    }
  };

  // ========== STATE ==========
  const LANG_KEY = 'vitanova_language';
  let currentLang = localStorage.getItem(LANG_KEY) || 'ar';

  // ========== CORE FUNCTIONS ==========
  
  /**
   * Get a translation by key
   */
  function t(key) {
    return translations[currentLang][key] || translations['ar'][key] || key;
  }

  /**
   * Get current language
   */
  function getLang() {
    return currentLang;
  }

  /**
   * Set language and apply translations
   */
  function setLang(lang) {
    if (lang !== 'ar' && lang !== 'en') {
      console.warn('Invalid language:', lang);
      return;
    }
    
    currentLang = lang;
    localStorage.setItem(LANG_KEY, lang);
    
    // Update document direction and lang attribute
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    document.body.dir = lang === 'ar' ? 'rtl' : 'ltr';
    
    // Apply translations to all elements with data-i18n
    applyTranslations();
    
    // Update language toggle button
    updateLangToggle();
    
    // Dispatch event for custom handlers
    window.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang } }));
  }

  /**
   * Toggle between languages
   */
  function toggleLang() {
    setLang(currentLang === 'ar' ? 'en' : 'ar');
  }

  /**
   * Apply translations to all elements with data-i18n attribute
   */
  function applyTranslations() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      const translation = t(key);
      
      // Handle different element types
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
        if (el.hasAttribute('placeholder')) {
          el.placeholder = translation;
        } else {
          el.value = translation;
        }
      } else if (el.tagName === 'OPTION') {
        el.textContent = translation;
      } else {
        // Check if we should use innerHTML (for translations with HTML)
        if (translation.includes('<b>') || translation.includes('<strong>')) {
          el.innerHTML = translation;
        } else {
          el.textContent = translation;
        }
      }
    });
    
    // Handle data-i18n-placeholder for inputs
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      const key = el.getAttribute('data-i18n-placeholder');
      el.placeholder = t(key);
    });
    
    // Handle data-i18n-title for titles
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
      const key = el.getAttribute('data-i18n-title');
      el.title = t(key);
    });
    
    // Handle data-i18n-aria for aria-label
    document.querySelectorAll('[data-i18n-aria]').forEach(el => {
      const key = el.getAttribute('data-i18n-aria');
      el.setAttribute('aria-label', t(key));
    });
  }

  /**
   * Update the language toggle button display
   */
  function updateLangToggle() {
    const toggleBtns = document.querySelectorAll('.lang-toggle');
    toggleBtns.forEach(btn => {
      // Show the CURRENT language code (what the site is in)
      const langText = btn.querySelector('.lang-text') || btn;
      if (langText.querySelector('svg')) {
        // Button has SVG, update only the text node
        const textNode = Array.from(btn.childNodes).find(
          node => node.nodeType === Node.TEXT_NODE && node.textContent.trim()
        );
        if (textNode) {
          textNode.textContent = currentLang.toUpperCase();
        } else {
          // Add text after SVG if not found
          btn.appendChild(document.createTextNode(' ' + currentLang.toUpperCase()));
        }
      } else {
        langText.textContent = currentLang.toUpperCase();
      }
    });
  }

  /**
   * Initialize the language system
   */
  function init() {
    // Apply saved language or default (Arabic)
    setLang(currentLang);
    
    // Set up language toggle buttons
    document.querySelectorAll('.lang-toggle').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        toggleLang();
      });
    });
  }

  // ========== PUBLIC API ==========
  return {
    t,
    getLang,
    setLang,
    toggleLang,
    init,
    translations // Expose for debugging
  };
})();

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', VitaNovaLang.init);
} else {
  VitaNovaLang.init();
}

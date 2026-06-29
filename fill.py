import os
import django
import random
from django.utils.text import slugify

# 1. تهيئة بيئة ديجانجو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from store.models import Product, Category

print("⏳ جاري إنشاء الأقسام وتوليد مئات المنتجات ديناميكيًا...")

# 2. إنشاء الأقسام مع الـ slug
categories_names = ["سيارات ومركبات", "ملابس وأزياء", "إلكترونيات وتقنية", "أدوات رياضية", "مستلزمات منزلية"]
categories = {}

for name in categories_names:
    slug_value = slugify(name, allow_unicode=True)
    if not slug_value:
        slug_value = name.replace(" ", "-")
        
    cat, _ = Category.objects.get_or_create(
        name=name,
        defaults={'slug': slug_value}
    )
    categories[name] = cat

# 3. قوالب البيانات
data_templates = {
    "سيارات ومركبات": [
        ("مرسيدس C300", "سيارة فاخرة بأداء قوي وتقنيات متطورة لراحة مثالية على الطريق.", 45000, "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=600"),
        ("بي إم دبليو M4", "سيارة رياضية خارقة توفر متعة قيادة وإثارة لا تُنسى.", 65000, "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=600"),
        ("تويوتا كورولا", "السيارة الأكثر اعتمادية واقتصادية في استهلاك الوقود في العالم.", 22000, "https://images.unsplash.com/photo-1621007947382-cc34a364450e?w=600"),
        ("BYD Seal الكهربائية", "سيارة كهربائية متطورة بتصميم انسيابي رياضي ينافس أقوى السيارات.", 35000, "https://images.unsplash.com/photo-1617788138017-80ad40651399?w=600"),
        ("تسلا موديل 3", "قيادة ذاتية بالكامل مع تسارع خارق وشاشة تحكم عملاقة ذكية.", 42000, "https://images.unsplash.com/photo-1563720223185-11003d516935?w=600")
    ],
    "ملابس وأزياء": [
        ("جاكيت شتوي عصري", "جاكيت مبطن عازل للمطر والبرد القارس بتصميم شيك جداً.", 80, "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600"),
        ("قميص كلاسيك فاخر", "قميص مصنوع من القطن الصافي 100% مناسب للمقابلات والعمل.", 35, "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600"),
        ("بنطلون جينز مريح", "جينز متين ومريح يتحمل الاستخدام اليومي الشاق والألوان ثابتة.", 45, "https://images.unsplash.com/photo-1542272604-787c3835535d?w=600"),
        ("حقيبة ظهر للمغامرات", "حقيبة ظهر مقاومة للماء مع جيب مخصص لحماية اللاب توب.", 55, "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600")
    ],
    "إلكترونيات وتقنية": [
        ("iPhone 15 Pro", "معالج A17 Pro الخارق مع كاميرا احترافية وتصميم تيتانيوم.", 1200, "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=600"),
        ("MacBook Pro M3", "لاب توب قوي جداً مخصص للمبرمجين والمصممين مع بطارية خارقة.", 2200, "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600"),
        ("سماعات سوني عازلة للصوت", "تجربة صوتية محيطية سينمائية مع أقوى نظام إلغاء ضوضاء.", 350, "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600"),
        ("شاشة قيمنق 144Hz", "ألوان فائقة الدقة وسرعة استجابة مذهلة لعشاق الألعاب.", 300, "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=600")
    ],
    "أدوات رياضية": [
        ("حذاء جري رياضي نايت", "وزن خفيف جداً ووسادة هوائية مريحة للمشي والجري الطويل.", 130, "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600"),
        ("طقم أثقال حديد منزلية", "مجموعة دامبلز قابلة للتعديل لتمارين القوة والبناء العضلي.", 90, "https://images.unsplash.com/photo-1638536532686-d610adfc8e5c?w=600"),
        ("ساعة ذكية للياقة البدنية", "تتبع نبضات القلب، السعرات، والخطوات اليومية مع مقاومة الماء.", 150, "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600")
    ],
    "مستلزمات منزلية": [
        ("ماكينة إسبريسو احترافية", "استمتع بقهوتك الصباحية بضغط 15 بار وفوم حليب مثالي.", 280, "https://images.unsplash.com/photo-1517256064527-09c53b2d0c6f?w=600"),
        ("مصباح مكتب ذكي LED", "إضاءة مريحة للعين مع إمكانية التحكم في درجات الألوان وقوة الضوء.", 40, "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=600")
    ]
}

# 4. توليد المنتجات
total_created = 0

for cat_name, products_list in data_templates.items():
    category_obj = categories[cat_name]
    
    for i in range(1, 31):
        base_product = random.choice(products_list)
        unique_title = f"{base_product[0]} (موديل {2026 + (i % 3)}) #إصدار-{i}"
        random_price_change = random.randint(-15, 50) if base_product[2] < 500 else random.randint(-500, 1000)
        final_price = max(10, base_product[2] + random_price_change)
        
        Product.objects.get_or_create(
            title=unique_title,
            defaults={
                "description": f"{base_product[1]} (نسخة مميزة رقم {i} خاضعة لفحص الجودة).",
                "price": final_price,
                "Category": category_obj,
                "image": base_product[3],
                "stock": random.randint(5, 50)  # الحل السحري: تم إضافة حقل الـ stock هنا بنجاح!
            }
        )
        total_created += 1

print(f"✅ مبروك يا فادي! تم ملء قاعدة البيانات بـ {total_created} منتج بنجاح وبدون أي أخطاء!")

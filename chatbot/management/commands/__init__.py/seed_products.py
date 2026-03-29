"""
Usage:
    python manage.py seed_products
"""

from django.core.management.base import BaseCommand
from chatbot.models import Product


SAMPLE_PRODUCTS = [
    {
        "name": "ProBook X15 Ultra",
        "category": "laptop",
        "icon": "💻",
        "badge": "New",
        "badge_type": "",
        "price": 1299.00,
        "description": "15.6\" OLED display, Intel Core i9, 32GB RAM, 1TB NVMe SSD.",
        "specs": {
            "Display": "15.6\" OLED 4K 120Hz",
            "Processor": "Intel Core i9-14900H",
            "RAM": "32GB DDR5",
            "Storage": "1TB NVMe SSD",
            "Battery": "86Wh, up to 12hr",
            "Weight": "1.8kg",
            "OS": "Windows 11 Pro"
        },
        "highlights": [
            "Industry-leading OLED display",
            "Thunderbolt 4 ports",
            "Military-grade durability"
        ]
    },
    {
        "name": "ZenPad Pro 12",
        "category": "tablet",
        "icon": "📱",
        "badge": "Hot",
        "badge_type": "hot",
        "price": 849.00,
        "description": "12\" AMOLED tablet with stylus support, perfect for creative work.",
        "specs": {
            "Display": "12\" AMOLED 2K 90Hz",
            "Processor": "Snapdragon 8 Gen 3",
            "RAM": "12GB LPDDR5",
            "Storage": "256GB UFS 4.0",
            "Battery": "10,000mAh",
            "Stylus": "Included ZenPen Pro",
            "OS": "Android 14"
        },
        "highlights": [
            "Pressure-sensitive stylus",
            "4-speaker surround",
            "IP68 waterproof"
        ]
    },
    {
        "name": "SoundCore ANC Pro",
        "category": "headphones",
        "icon": "🎧",
        "badge": "Sale",
        "badge_type": "",
        "price": 249.00,
        "description": "Premium wireless headphones with 40dB active noise cancellation.",
        "specs": {
            "Type": "Over-ear, Closed-back",
            "Connectivity": "Bluetooth 5.3 / 3.5mm",
            "ANC Level": "Up to 40dB reduction",
            "Battery Life": "Up to 30 hours",
            "Charging Time": "2 hours (USB-C)",
            "Drivers": "40mm custom dynamic",
            "Weight": "250g"
        },
        "highlights": [
            "Foldable design for travel",
            "Hi-Res Audio certified",
            "Multipoint connection"
        ]
    },
    {
        "name": "VisionWatch Ultra",
        "category": "smartwatch",
        "icon": "⌚",
        "badge": "New",
        "badge_type": "",
        "price": 399.00,
        "description": "Advanced health tracking smartwatch with ECG and blood oxygen sensor.",
        "specs": {
            "Display": "1.4\" AMOLED Always-on",
            "Processor": "Exynos W930",
            "RAM": "2GB / 16GB storage",
            "Battery": "Up to 5 days",
            "Sensors": "ECG, SpO2, GPS, Gyro",
            "Water Resistance": "5ATM + IP68",
            "Compatibility": "Android & iOS"
        },
        "highlights": [
            "FDA-cleared ECG sensor",
            "Sleep & stress tracking",
            "100+ workout modes"
        ]
    },
    {
        "name": "NovaCam 8K Pro",
        "category": "camera",
        "icon": "📷",
        "badge": "New",
        "badge_type": "",
        "price": 2199.00,
        "description": "Mirrorless 8K camera for professional photographers and videographers.",
        "specs": {
            "Sensor": "Full-Frame BSI-CMOS",
            "Resolution": "45MP / 8K video",
            "ISO": "100-51200 (expandable)",
            "Stabilization": "7-stop IBIS",
            "AF Points": "759-point phase-detect",
            "Recording": "8K30 / 4K120 RAW",
            "Battery": "720 shots per charge"
        },
        "highlights": [
            "Dual card slots",
            "Weather-sealed body",
            "60fps burst shooting"
        ]
    },
    {
        "name": "ArcMini Gaming PC",
        "category": "desktop",
        "icon": "🖥️",
        "badge": "Hot",
        "badge_type": "hot",
        "price": 1599.00,
        "description": "Compact yet powerful gaming desktop. RTX 4070 in a mini-ITX form.",
        "specs": {
            "Processor": "AMD Ryzen 9 7950X",
            "GPU": "NVIDIA RTX 4070 Ti",
            "RAM": "64GB DDR5 6000MHz",
            "Storage": "2TB PCIe 5.0 NVMe",
            "Form Factor": "Mini-ITX",
            "Connectivity": "WiFi 7, BT 5.4",
            "PSU": "850W 80+ Gold"
        },
        "highlights": [
            "Whisper-quiet cooling",
            "RGB customizable",
            "VR ready"
        ]
    },
]


class Command(BaseCommand):
    help = 'Seed the database with sample tech products'

    def handle(self, *args, **kwargs):
        if Product.objects.exists():
            self.stdout.write(self.style.WARNING('Products already exist. Skipping seed.'))
            return

        for data in SAMPLE_PRODUCTS:
            Product.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {data["name"]}'))

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Seeded {len(SAMPLE_PRODUCTS)} products successfully!'
        ))
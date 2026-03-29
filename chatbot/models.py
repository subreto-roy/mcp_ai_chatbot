from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('laptop', 'Laptop'),
        ('tablet', 'Tablet'),
        ('headphones', 'Headphones'),
        ('smartwatch', 'Smartwatch'),
        ('camera', 'Camera'),
        ('desktop', 'Desktop'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    icon = models.CharField(max_length=10, default='')
    badge = models.CharField(max_length=30, blank=True)
    badge_type = models.CharField(max_length=20, blank=True)  # 'hot', 'sale', etc.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    specs = models.JSONField(default=dict)       # {"RAM": "32GB", "CPU": "i9"}
    highlights = models.JSONField(default=list)  # ["Feature 1", "Feature 2"]
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def price_display(self):
        return f"${self.price:,.0f}"
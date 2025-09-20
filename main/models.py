import uuid
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('jersey', 'Jersey'),
        ('aksesoris', 'Aksesoris'),
        ('sepatu', 'Sepatu'),
        ('topi', 'Topi'),
        ('badge', 'Badge')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    name = models.CharField(max_length=100, default="Empty")
    price = models.PositiveIntegerField(default=0)
    description = models.TextField(default="Empty")
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='jersey')
    is_featured = models.BooleanField(default=False)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    views = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    brand = models.CharField(max_length=50, default="Unknown")
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    
    def __str__(self):
        return self.name
    
    @property
    def is_stock_available(self):
        return self.stock > 0
    
    def increment_views(self): 
        self.views += 1 
        self.save() 
        
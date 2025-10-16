from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    making_charges = models.DecimalField(max_digits=10, decimal_places=2,  default=500.00)
    wastage_percent = models.DecimalField(max_digits=5, decimal_places=2, default=15.00)
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_description = models.TextField()
    weight = models.DecimalField(max_digits=5, decimal_places=3)
    img_url = models.ImageField(null=True, upload_to='products/images')
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)
    
    @property
    def formatted_url(self):
        url = self.img_url if self.img_url.__str__().startswith(('https://','http://')) else self.img_url.url
        return url
    
    def current_price(self):
        from .models import GoldRate
        latest_rate = GoldRate.objects.latest('date')
        today_rate = latest_rate.rate_per_gram 

        weight = self.weight + (self.weight * (self.category.wastage_percent/100))
        Amount = weight * today_rate 
        total = Amount + self.category.making_charges
        return round(total,0)
        
    def __str__(self):
        return self.product_name
    

class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favourites")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,  related_name='favourited_by')
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user','product')
        
    def __str__(self):
        return f"{self.user.username} favourited  {self.product.product_name}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Cart"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('cart','product')
    
    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} * {self.product.product_name}"
        
class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('shipment', 'By Shipment'),
        ('in_person', 'In Person'),
    ]

    # Customer info
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    # Order type
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES)

    # Shipment details (optional)
    shipping_address = models.CharField(max_length=255, blank=True, null=True)
    shipping_city = models.CharField(max_length=100, blank=True, null=True)
    shipping_state = models.CharField(max_length=100, blank=True, null=True)
    shipping_zip = models.CharField(max_length=10, blank=True, null=True)

    # Billing details - Deleted

    # In-person pickup info (fixed, but you can store it too)
    pickup_location = models.CharField(max_length=255, default="Sri Sangunthala Jewellery, Karur")

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.email}"


class GoldRate(models.Model):
    date = models.DateField(default=timezone.now, unique=True)
    rate_per_gram = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.date} - ₹{self.rate_per_gram}"
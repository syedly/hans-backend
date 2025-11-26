from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        extra_fields.setdefault("username", email)  # fallback username
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Remove username as login field, but keep field present
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # still asked when creating superuser

    objects = CustomUserManager()

    class Meta:
        db_table = "Users"

    def __str__(self):
        return self.email
    
class Purchase(models.Model):
    # Original API id
    external_id = models.IntegerField(unique=True)

    # --- Purchase Fields ---
    purchase_date = models.IntegerField()
    purchase_month = models.CharField(max_length=20)
    purchase_year = models.IntegerField()

    province = models.CharField(max_length=50, null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    last_digits = models.CharField(max_length=4, null=True, blank=True)
    shipping_address = models.TextField(null=True, blank=True)

    # --- User Fields ---
    user_id = models.IntegerField()
    user_username = models.CharField(max_length=150)
    user_first_name = models.CharField(max_length=150)
    user_last_name = models.CharField(max_length=150)
    user_email = models.EmailField()

    # --- Product Fields ---
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=200)
    product_description = models.TextField(null=True, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image_url = models.URLField(max_length=500, null=True, blank=True)

    product_is_available = models.BooleanField()
    product_status = models.CharField(max_length=50, null=True, blank=True)
    product_category = models.CharField(max_length=50, null=True, blank=True)
    product_sku = models.CharField(max_length=50, null=True, blank=True)
    product_stock = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.product_name} ({self.user_username})"

class Product(models.Model):
    external_id = models.IntegerField(unique=True)

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    price = models.FloatField(null=True, blank=True)
    discounted_price = models.FloatField(null=True, blank=True)

    is_available = models.BooleanField(default=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    sku = models.CharField(max_length=100, null=True, blank=True)

    stock = models.IntegerField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

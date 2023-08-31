from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator
from django.utils.text import slugify


class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, address, phone_number, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, address=address, phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, address, phone_number, password=None):
        user = self.create_user(email, full_name, address, phone_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    #ACCOUNT_TYPES = [
    #    ('buyer', 'Buyer'),
    #    ('seller', 'Seller'),
    #]
    username = None
    full_name = models.CharField(max_length=255)
    #account_type = models.CharField(max_length=6, choices=ACCOUNT_TYPES, default='buyer')
    email = models.EmailField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'address', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.full_name


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, default="")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(validators=[MinValueValidator(0.01)])
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True)
    details = models.CharField(max_length=255)
    side_effects = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/')
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, default="")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        unique_together = ["user", "slug"]

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(to=Product, through="ProductCart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.full_name}'s cart"


class ProductCart(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.product} ({self.quantity})"


class Order(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(to=Product, through="ProductOrder")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.full_name}'s order"


class ProductOrder(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.product} ({self.quantity})"

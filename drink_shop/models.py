from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField('Title', max_length=100)
    cover = models.ImageField('Cover', upload_to='category_covers', null=True)
    featured = models.BooleanField('Featured')
    active = models.BooleanField('Active')
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(str(self.id))
            self.save()

        super().save(*args, **kwargs)
        img = Image.open(self.cover.path)

        if img.height > 1 or img.width > 1:
            output_size = (400, 400)
            img.resize(output_size)
            img.save(self.cover.path)

    def get_url(self):
        return reverse("drink_shop:product_by_category", kwargs={
            'slug': self.slug
        })


class Product(models.Model):
    title = models.CharField('Title', max_length=100)
    description = models.TextField('Description', max_length=2000, null=True, blank=True)
    price = models.DecimalField('Price', max_digits=10, decimal_places=2, null=True, blank=True)
    cover = models.ImageField('Cover', upload_to='product_covers', null=True)
    featured = models.BooleanField('Featured', default=False)
    active = models.BooleanField('Active', default=False)
    product_region = models.CharField('Product region', max_length=100, null=True, blank=True)
    abv = models.FloatField('ABV', null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.title}"

    def get_url(self):
        return reverse("drink_shop:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("drink_shop:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("drink_shop:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(str(self.id))
            self.save()

        super().save(*args, **kwargs)
        img = Image.open(self.cover.path)

        if img.height > 1 or img.width > 1:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.cover.path)


class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"

    def get_total_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey("ShippingAddress", on_delete=models.SET_NULL, blank=True, null=True)

    def get_final_price(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_total_price()
        return total


class Comment(models.Model):
    post = models.ForeignKey(Product, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)


class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100, blank=True, null=True)
    apartment_address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username
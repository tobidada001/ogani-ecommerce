from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.safestring import mark_safe
from math import floor
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
import uuid

# Create your models here.

class Category(models.Model):
    cat_name = models.CharField(max_length=100, unique=True)
    cat_slug = models.SlugField( max_length= 300, unique= True)
    thumbnail = models.ImageField(upload_to='categories', blank=True, null=True)

    class Meta:
        verbose_name_plural = ("Categories")

    def __str__(self):
        return self.cat_name

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.cat_slug})
    
    def save(self, *args, **kwargs):
       self.cat_slug = slugify(self.cat_slug)
       super(Category, self).save(*args, **kwargs) 
    

class Color(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    def generated_color(self):
        return mark_safe(f'<div style="background-color: {self.name}; border: 2px solid black; height: 20px; width: 100px;"></div>')


class SaleOffProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(price__gt = models.F('current_price'))
    
class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter()


class Wishlist(models.Model):
    product = models.ForeignKey("Product", on_delete=models.SET_DEFAULT, default="Product not available")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return str(self.owner) + ' added new product to wishlist.'
    

class Review(models.Model):

    review_ratings = (("5", "★★★★★" ),
                      ("4", "★★★★☆"),
                      ("3", "★★★☆☆"),
                      ("2", "★★☆☆☆"),
                      ("1", "★☆☆☆☆"))

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    rating = models.CharField(max_length=50, choices= review_ratings, default="3")

    def __str__(self):
        return str(self.owner.username)


class Product(models.Model):
    # VARIANTS = (('Color', 'Color'), ('Size', 'Size'), ('Size-Color', 'Size-Color'), ('None', 'None'))
    name = models.CharField(verbose_name = "Product Name", max_length=100)
    price = models.FloatField()
    current_price = models.FloatField(default= 0)
    description = RichTextUploadingField()
    image = models.ImageField(verbose_name = "Product image", upload_to='products/')
    featured = models.BooleanField(default= False)
    featured_image = models.ImageField(upload_to="products/featured_images/", blank=True, null=True)
    # is_new = models.BooleanField(default = True)
    sales = models.PositiveIntegerField(default = 0)
    sku = models.CharField(max_length=10)
    objects = ProductManager()
    saleoffproducts = SaleOffProductManager()

    # variant = models.CharField(max_length=15, choices = VARIANTS, default = 'None')
    
    category = models.ForeignKey(Category, related_name = 'products', on_delete=models.CASCADE)
    # brand = models.ForeignKey("ecommerce.Brand", related_name = 'brand_products', verbose_name=("Brand"), blank=True, null=True, on_delete=models.CASCADE)
    date_added = models.DateTimeField(verbose_name="Date Added", auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name="Last Updated", auto_now=True)


    @property
    def calculate_percent_off(self):
        discount = self.price - self.current_price
        percentage = floor((discount / self.price) * 100)
        return f"{percentage}"
   
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-date_added',)

    

class Order(models.Model):
    choices = (('completed', 'Completed'), ('paid', 'Paid'), ('pending', 'Pending Payment'))
    name = models.CharField(max_length=100)
    email = models.EmailField( max_length=254)
    status = models.CharField(max_length=50, choices= choices, default='pending')
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField( max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length= 15, blank=True, null=True)
    shippingaddress= models.CharField(max_length=200, blank=True, null=True)
    order_notes= models.TextField(blank=True, null=True)
    method = models.CharField(max_length=50, blank=True, null=True)
    
    sessionid = models.CharField(max_length=200, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    

    def __str__(self):
        return self.name
    
   
    


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField()
    total_price = models.FloatField()
    order = models.ForeignKey("Order", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'Order {self.id}'


# class ProductImage(models.Model):
#     product= models.ForeignKey(Product, on_delete=models.SET_NULL, null = True)
#     image = models.ImageField(upload_to='product_image/')
#     def __str__(self):
#         return 'Image: ' +self.product.name


class NewsletterEmail(models.Model):
    email = models.EmailField(max_length=254)


class Contact(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=254)
    message = models.TextField()
    
    def __str__(self):
        return self.name



# ************************************ BLOG *************************
class PostCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()


class Post(models.Model):
    status = (('draft', 'Draft'), ('published', 'Published'))
    title = models.CharField(max_length=150, unique=True)
    body = RichTextUploadingField()
    cover = models.ImageField(upload_to='blogpost/')
    post_status = models.CharField(max_length=50, choices=status, default="published")
    slug = models.SlugField(unique=True)
    category = models.ForeignKey("PostCategory",  on_delete=models.CASCADE)
    tags = TaggableManager()
    date_posted= models.DateTimeField(auto_now=False, auto_now_add=True)

    def save(self, *args, **kwargs):
       
       if not self.slug:
           self.slug = slugify(self.title)
       
       super(Post, self).save(*args, **kwargs) # Call the real save() method

    def __str__(self):
        return self.title
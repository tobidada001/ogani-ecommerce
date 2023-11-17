from django.contrib import admin

from Shop.models import Order, Product
from . import models
# Register your models here.

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('cat_name',)
    prepopulated_fields = {'cat_slug': ['cat_name']}

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'status', 'owner']
    list_editable = ('status',)


@admin.register(models.Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'generated_color')

admin.site.register(Product)
admin.site.register(models.Contact)
admin.site.register(models.Wishlist)
admin.site.register(models.OrderItem)
admin.site.register(models.Review)
admin.site.register(models.NewsletterEmail)

#blog
@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}

    
admin.site.register(models.PostCategory)

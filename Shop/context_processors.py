
from .models import Category, NewsletterEmail, Product, Wishlist
import random
from django.contrib import messages
from django.shortcuts import redirect
from Shop.models import PostCategory
from taggit.models import Tag
def contexts(request):

    if request.method == 'POST':
        if request.POST.get('newsletteremail'):
            NewsletterEmail.objects.create(email = request.POST['newsletteremail'])
            messages.success(request, "You have successfully subscribed to our newsletter.")


    categories = Category.objects.all()
    products_retrieved = Product.objects.all()
    randnum = random.randint(0, products_retrieved.count() - 1)
    categories = PostCategory.objects.all()
    tags = Tag.objects.all()
    large_featured_product = products_retrieved.all()[randnum]


    try:
        wishlist_total = Wishlist.objects.filter(owner = request.user).count()
    except:
        wishlist_total = 0

    

    return {'categories' : categories, 'total_in_wishlist': wishlist_total, 'large_fp': large_featured_product, 'categories': categories, 'tags': tags }
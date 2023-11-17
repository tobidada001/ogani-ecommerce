from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q, Avg, Sum
from paypal.standard.forms import PayPalPaymentsForm
import random
import json
from taggit.models import Tag
# Create your views here.

def index(request):
    featured_products = Product.objects.filter(featured = False)
    products_retrieved = Product.objects.all()

    products = products_retrieved.order_by('-date_added')
    toprated = products_retrieved.annotate(avgrating = Avg('review__rating')).order_by('-avgrating')[:6]
    most_reviewed = products_retrieved.annotate(count= Count('review')).order_by('-count')[:6]

    return render(request, 'index.html', {'featured': featured_products, 'products': products, 'top_rated': toprated, "most_reviewed": most_reviewed })


def login(request):
    return render(request, 'login.html')

def shop(request):
    colors = Color.objects.all()
    saleoffprods = Product.saleoffproducts.all()
    products = Product.objects.all()
    latest_prod = Product.objects.filter().order_by('-id')[:6]

    pages = Paginator(products, 10)
    
    page_number = request.GET.get('page', 1)
    page = pages.get_page(page_number)
    page.adjusted_elided_pages = pages.get_elided_page_range(page_number)


    return render(request, 'shop-grid.html', { 'colors' : colors, 'saleoffprods': saleoffprods, 'products': products, 'latest_prod': latest_prod, 'page': page})


def product_detail(request, pk):
    product = get_object_or_404(Product, id = pk)
    category = get_object_or_404(Category, id = product.category.id)
    print('Category: ', category)
    return render(request, 'shop-details.html', {'product': product, 'category': category})

def search_product(request):

    if request.GET.get('q'):
        products = Product.objects.filter(name__icontains = request.GET['q'])
        print(f'Products named {request.GET.get("q")}: ', products )
    else:
        products = Product.objects.all()    

    pages = Paginator(products, 2)
    
    page_number = request.GET.get('page', 1)
    page = pages.get_page(page_number)
    page.adjusted_elided_pages = pages.get_elided_page_range(page_number)

    return render(request, 'searchpage.html', {'products': products, 'page': page})


def add_to_cart(request):
    return HttpResponse('REst, bro.')

def category_detail(request, id):

    category = get_object_or_404(Category, id = id)
    colors = Color.objects.all()
    latest_prod = Product.objects.filter().order_by('-id')[:6]
    return render(request, 'category.html', {'category': category,'colors' : colors, 'latest_prod': latest_prod})

def cart(request):
    return render(request, 'shoping-cart.html')


@login_required(login_url='/login/')
def wishlist(request):
    wishlist = Wishlist.objects.filter(owner = request.user)

    if request.GET.get('wishlistid'):
        product = get_object_or_404(Product, id= request.GET['wishlistid'])
        if not Wishlist.objects.filter(owner = request.user, product= product).exists():
            Wishlist.objects.create(owner = request.user, product = product)
            return JsonResponse({'added': True, 'wishlistcount': Wishlist.objects.filter(owner = request.user).count()})
           
        else:
            return JsonResponse({'added': False})
    
    if request.GET.get('wid'):
        wish = get_object_or_404(Wishlist, id = request.GET['wid'])
        wish.delete()

        wishlists = Wishlist.objects.filter(owner = request.user)

        return JsonResponse({'wishlistcount': wishlists.count(), 'wishlists': list(wishlists.values('id', 'product__name', 'product__price', 'product__image'))}, safe=True)

    return render(request, 'wishlists.html', {'wishlist': wishlist})



def create_payment(request):
    pay_amount = 0
    order = None
    if request.session.get('cur_sess_orderid'):
        order = get_object_or_404(Order, id = request.session['cur_sess_orderid'])
        pay_amount = order.order_items_set.aggregate(total_sum =Sum('total_price'))



 # What you want the button to do.
    paypal_dict = {
    "business": settings.PAYPAL_RECEIVER_EMAIL,
    "amount": f"{float(pay_amount)}",
    "item_name": f"Order TODAY",
    "invoice": f"INV-CART-{order.id}",
    "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
    "return": request.build_absolute_uri(reverse('payment_completed')),
    "cancel_return": request.build_absolute_uri(reverse('payment_failed')),
    # "custom": "premium_plan", # Custom command to correlate to some function
    }


    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment.html", context)


def payment_completed(request):
    if request.session.get('cur_sess_orderid'):
        order = get_object_or_404(Order, id = request.session['cur_sess_orderid'])
        order.status = 'paid'
        order.save()
    return render(request, 'payment_completed.html')


def payment_failed(request):
    return render(request, 'payment_failed.html')


def checkout(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        res_address = request.POST.get('res_address')
        apartment_address = request.POST.get('apartment_address')
        city = request.POST.get('city')
        zip = request.POST.get('zip')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        acc_password = request.POST.get('acc_password')
        shippingaddress = request.POST.get('shippingaddress')
        order_notes = request.POST.get('order_notes')
        cartitems = request.POST.get('cartitems')
        method = request.POST.get('method')
        name = f"{firstname} {lastname}"
        full_home_address = f'{res_address} \n {apartment_address}'
        
        if cartitems:
            request.session['cur_sess_cart_data'] = json.loads(cartitems)

        
        order = Order.objects.create(name = name, email = email, address = full_home_address, city = city, country = country, zip = zip, 
                                     shippingaddress = shippingaddress, order_notes = order_notes, method = method)
        
        user = None

        if request.user.is_authenticated:
            user = request.user

        elif acc_password:
            if User.objects.filter(Q(email = email)).exists():
                user = User.objects.filter(Q(email = email)).first()
            else:
                user = User(username = email.split('@')[0], email = email, first_name =firstname, last_name = lastname)
                user.set_password(acc_password)
                user.save()

        order.owner = user 
        order.save()
        

        if request.session.get('cur_sess_cart_data'):
            for id, data in json.loads(request.session.get('cur_sess_cart_data')).items():
                product = Product.objects.get(id = id)
                total_price  = float(product.price * int(data['quantity']))
                orderitem = OrderItem( product = product, quantity = data['quantity'] , total_price= total_price, order =order   )
                orderitem.save()
            

        if request.POST.get('method') == 'paypal':
            request.session['cur_sess_orderid'] = order.id
            return redirect('create_payment')
        
        elif request.POST.get('method') == 'check':
            return redirect('cart')
        
    return render(request, 'checkout.html')

def post_detail(request, slug):
    post = get_object_or_404(Post, slug= slug)
    posts = Post.objects.all()
    recent_posts = posts.order_by('-date_posted')[:3]
    random_posts = posts.order_by('?')

    return render(request, 'blog-details.html', {'post': post, 'posts': posts, 'recent_posts': recent_posts, 'random_posts': random_posts})


def blog(request):
    posts = Post.objects.all()
    recent_posts = posts.order_by('-date_posted')[:3]
    random_posts = posts.order_by('?')
   
    return render(request, 'blog.html', {'posts': posts, 'recent_posts': recent_posts, 'random_posts': random_posts})


def contact(request):
    if request.method == 'POST':
        Contact.objects.create(name = request.POST['name'], email = request.POST['email'], message = request.POST['message'])
        messages.success(request, 'Hi there! Thank you for messaging us.')
        return redirect('/')
    return render(request, 'contact.html')

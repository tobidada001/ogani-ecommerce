from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('shop', views.shop, name = 'shop'),
    path('product-detail/<int:pk>/', views.product_detail, name= 'detail'),
    path('cart', views.cart, name= 'cart'),
    path('checkout', views.checkout, name= 'checkout'),
    path('postdetail', views.post_detail, name='postdetail'),
    path('blog', views.blog, name = 'blog'),
    path('contact', views.contact, name= 'contact'),
    path('category/<int:id>/', views.category_detail, name = 'category'),
    path('search/', views.search_product, name= 'search'),
    path('add-to-cart/', views.add_to_cart, name= 'add_to_cart'),
    path('wishlist', views.wishlist, name='wishlist'),

    #auth user
    path('login', views.login, name='login'),

    #payment
    path('create_payment', views.create_payment, name='create_payment'),
    path('payment_completed', views.payment_completed, name = 'payment_completed'),
    path('payment_failed', views.payment_failed, name= 'payment_failed'),


    #blog

    path('blog', views.blog, name='blogposts'),
    path('post-detail/<slug:slug>/', views.post_detail, name = 'postdetail')
]

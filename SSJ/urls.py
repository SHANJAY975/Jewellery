from django.urls import path
from . import views

app_name = "SSJ"
urlpatterns = [
    path('',views.index, name='landing_page'),
    path('about_us', views.about_us, name="about"),
    path('necklaces', views.necklaces, name="necklaces"),
    path('details/<str:slug>', views.details, name="details"),
    path('details/<str:slug>/favourite/', views.toggle_favourite, name='toggle_favourite'),
    path('sign_up', views.sign_up, name="sign_up"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('forgot_password', views.forgot_password, name="forgot_password"),
    path('reset_password/<uidb64>/<token>', views.reset_password, name="reset_password"),
    path('add_product', views.add_product, name="add_product"),
    path('cart/add/<str:slug>/', views.add_to_cart, name='add_to_cart'),
    path('cart/delete/<int:item_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('review_checkout',views.review_checkout, name="review_checkout"),
    path('checkout',views.checkout, name="checkout"),
    path('all_products',views.all_products, name="all_products"),
    path('rings', views.rings, name="rings"),
    path('bracelets', views.bracelets, name="bracelets"),
    path('earrings', views.earrings, name="earrings"),
    path('gold_rate', views.gold_rate, name="gold_rate"),
    path("success/", views.payment_success, name="payment_success"),
    path('verify_payment', views.verify_payment, name='verify_payment'),
    path("generate/", views.generate_jewellery_image, name="generate_jewellery_image"),
]


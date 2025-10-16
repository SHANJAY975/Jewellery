from django.shortcuts import render, redirect, get_object_or_404
from SSJ.models import Cart, CartItem, Category, Favourite, GoldRate, Product
from django.http.response import HttpResponse
from django.core.paginator import Paginator
from .forms import AddProductForm, ForgotPasswordForm, RegisterForm, LoginForm, ResetPasswordForm, OrderForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
import razorpay
from django.conf import settings
from .context_processors import cart
import base64
import os
import requests
from django.core.files.storage import default_storage

api_key = settings.API_KEY

# Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# Create your views here.
def sign_up(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #user data created
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration Successfull. You can Log in")
            return render(request, 'index.html', {'form':form,'show_Login_modal': True})
    # next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/"
    return render(request, 'index.html', {'form':form,'show_signup_modal': True })

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                print("Login Success")
                return redirect("SSJ:necklaces")
    return render(request, 'index.html', {'form':form, 'show_Login_modal': True})       

def index(request):
    return render(request, 'index.html')

def all_products(request):
    products = Product.objects.all()
    Title = 'All Products'
    Sub_description = "Lorem ipsum dolor sit amet."
    return render(request, 'product_view.html',{'products':products, 'Title':Title, 'Sub_description':Sub_description})

def rings(request):
    category = Category.objects.get(name="rings")
    products = Product.objects.filter(category = category)
    Title = 'Rings'
    Sub_description = "Lorem ipsum dolor sit amet."
    return render(request, 'product_view.html',{'products':products, 'Title':Title, 'Sub_description':Sub_description})

def bracelets(request):
    category = Category.objects.get(name="bracelets")
    products = Product.objects.filter(category = category)
    Title = 'Bracelets'
    Sub_description = "Lorem ipsum dolor sit amet."
    return render(request, 'product_view.html',{'products':products, 'Title':Title, 'Sub_description':Sub_description})

def earrings(request):
    category = Category.objects.get(name="earrings")
    products = Product.objects.filter(category=category)
    Title = 'Earrings'
    Sub_description = "Lorem ipsum dolor sit amet."
    return render(request, 'product_view.html',{'products':products, 'Title':Title, 'Sub_description':Sub_description})


def necklaces(request):
    category = Category.objects.get(name="necklaces")
    products = Product.objects.filter(category=category)
    Title = 'Necklaces'
    Sub_description = "Lorem ipsum dolor sit amet."
    return render(request, 'product_view.html',{'products':products, 'Title':Title, 'Sub_description':Sub_description})

def about_us(request):
    return render(request, 'about_us.html')

def details(request, slug):
    product = get_object_or_404(Product, slug=slug)
    # Related products 
    related_products = Product.objects.exclude(pk=product.id)
    # Paginator
    paginator = Paginator(related_products, 5)
    page_no = request.GET.get('page')
    page_obj = paginator.get_page(page_no)

    in_cart = False
    is_favourite = False
    if request.user.is_authenticated:
        is_favourite = Favourite.objects.filter(user=request.user, product=product).exists()
        cart, _ = Cart.objects.get_or_create(user=request.user)
        in_cart = CartItem.objects.filter(cart=cart, product=product).exists()

    price = product.current_price
    return render(request, 'details.html', {
        'product': product,
        'page_obj': page_obj,
        'is_favourite': is_favourite,
        'in_cart':in_cart,
        'price':price,
    })

@login_required
def toggle_favourite(request, slug):
    product = get_object_or_404(Product, slug=slug)
    favourite, created = Favourite.objects.get_or_create(user=request.user, product=product)
    if not created:
        # already favourited -> remove
        favourite.delete()

    return redirect('SSJ:details', slug=slug)

@login_required
def add_to_cart(request, slug):
    if request.method == "POST":
        product = Product.objects.get(slug=slug)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()
                
    return redirect('SSJ:details', slug=slug)

@login_required
def delete_from_cart(request, item_id):
    if request.method == "POST":
        cartitem = get_object_or_404(CartItem, id=item_id) 
        cartitem.delete()
    previous_url = request.META.get('HTTP_REFERER')
    return redirect(previous_url)
    


def logout(request):
    auth_logout(request)
    return redirect("SSJ:landing_page")


def forgot_password(request):
    form = ForgotPasswordForm()
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            
            #send reset email to user
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            domain = current_site.domain
            subject = 'Reset Password'
            message = render_to_string('reset_password_mail.html', {'domain':domain, 'uid':uid, 'token':token})
            send_mail(subject=subject, message=message, from_email=None, recipient_list=[email] )
            messages.success(request, 'Reset mail has been sent')
    return render(request, 'forgot_password.html', {'form':form})


def reset_password(request, uidb64, token):
    resetform = ResetPasswordForm()
    if request.method == 'POST':
        resetform = ResetPasswordForm(request.POST)
        if resetform.is_valid():
            new_password = resetform.cleaned_data['new_password']
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, User.DoesNotExist, OverflowError):
                user = None
            
            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been reset Successfully')
                return redirect('SSJ:login')
            else:
                messages.error(request, 'Invalid Link')
                return redirect('SSJ:forgot_password')
    return render(request,'reset_password.html', {'form':resetform})


def add_product(request):
    addproductform = AddProductForm()
    if request.method == 'POST':
        addproductform = AddProductForm(request.POST, request.FILES)
        if addproductform.is_valid():
            product = addproductform.save()
            return redirect('SSJ:necklaces')
        
    categories = Category.objects.all()
    return render(request, 'add_product.html', {'categories':categories, 'addproductform': addproductform})

def review_checkout(request):
    return render(request, "checkout_review.html")

def checkout(request):
    orderform = OrderForm()
    open_razorpay = False
    razorpay_order = None

    if request.method == 'POST':
        orderform = OrderForm(request.POST)
        if orderform.is_valid():
            order = orderform.save()
            total_context = cart(request)
            # Example amount (replace with your cart total)
            total = total_context['total']
            print(total)
            amount = int(total * 100)
            currency = "INR"
            razorpay_order = razorpay_client.order.create({
                "amount": amount,
                "currency": currency
            })
            order.razorpay_order_id = razorpay_order["id"]
            order.save()

            open_razorpay = True  # tell template to trigger Razorpay popup

    context = {
        "orderform": orderform,
        "key_id": settings.RAZORPAY_KEY_ID,
        "open_razorpay": open_razorpay,
        "razorpay_order": razorpay_order
    }
    return render(request, "checkout.html", context)

def gold_rate(request):
    rate = GoldRate.objects.latest('date')
    return HttpResponse(rate)

def verify_payment(request):
    if request.method == "POST":
        payment_id = request.POST.get("razorpay_payment_id")
        order_id = request.POST.get("razorpay_order_id")
        signature = request.POST.get("razorpay_signature")

        try:
            razorpay_client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature
            })
            return redirect("SSJ:payment_success")
        except razorpay.errors.SignatureVerificationError:
            return HttpResponseBadRequest("Signature verification failed")
    return HttpResponseBadRequest("Invalid request")

def payment_success(request):
    """Render success page"""
    return render(request, "success.html")

def generate_jewellery_image(request):
    generated_image_url = None
    user = request.user

    if request.method == "POST":
        user_description =  request.POST.get("prompt")
        # Template prompt that enforces style, composition, and background
        full_prompt = f"Generate image of 22k gold ornaments with white background. Description:{user_description}"
        engine_id = "stable-diffusion-xl-1024-v1-0"

        response = requests.post(
            f"https://api.stability.ai/v1/generation/{engine_id}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "text_prompts": [{"text": user_description}],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
            },
        )

        if response.status_code == 200:
            data = response.json()
            image_data = data["artifacts"][0]["base64"]
            
            # Save image to MEDIA_ROOT
            output_dir = os.path.join(settings.MEDIA_ROOT, "generated")
            os.makedirs(output_dir, exist_ok=True)
            file_path = os.path.join(output_dir, "generated_image.png")
            
            with open(file_path, "wb") as f:
                f.write(base64.b64decode(image_data))
            
            generated_image_url = default_storage.url(f"generated/generated_image.png")
        else:
            return render(request, "generate.html", {"error": response.text})

    return render(request, "generate.html", {"generated_image_url": generated_image_url})
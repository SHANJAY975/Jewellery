from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import re
from SSJ.models import Category, Product, Order

class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=100, required=True)
    email = forms.CharField(label="Email",max_length=100, required=True)
    password = forms.CharField(label="Password",max_length=100, required=True)
    password_confirm = forms.CharField(label="Confirm_password",max_length=100, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
    
    
class LoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=100, required=True)
    password = forms.CharField(label="password", max_length=100, required=True)
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Invalid Credentials')
            
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="email", max_length=254, required=True)
    
    def clean(self):
        cleaned_data =  super().clean()
        email = cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('User not Found')
        

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(label="New Password", min_length=8)
    confirm_password = forms.CharField(label="Confirm Password", min_length=8)
    def clean(self):
       cleaned_data = super().clean()
       new_password = cleaned_data.get('new_password')
       confirm_password = cleaned_data.get('confirm_password')
       
       if new_password and confirm_password and new_password != confirm_password:
           raise forms.ValidationError('Password Does not Match')
       
       
class AddProductForm(forms.ModelForm):
    product_name = forms.CharField(label='product_name', max_length=100, required=True)
    product_description = forms.CharField(label='product_description', required=True)
    weight = forms.DecimalField(label='weight', decimal_places=3, required=True)
    category = forms.ModelChoiceField(label='category', required=True, queryset= Category.objects.all())
    img_url = forms.ImageField(label='Image', required=True)
    
    class Meta:
        model = Product
        fields = ['product_name', 'product_description', 'weight', 'img_url', 'category']
        

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'email', 'phone', 'address', 'city', 'state', 'zip_code',
            'order_type',
            'shipping_address', 'shipping_city', 'shipping_state', 'shipping_zip',
        ]

        widgets = {
            'order_type': forms.RadioSelect(choices=Order.ORDER_TYPE_CHOICES),
        }

    # 🔹 Field-level validations
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^[0-9]{10,15}$', phone):
            raise forms.ValidationError("Enter a valid phone number (10–15 digits).")
        return phone


    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')
        if not re.match(r'^[0-9]{5,10}$', zip_code):
            raise forms.ValidationError("Enter a valid ZIP code.")
        return zip_code

    # 🔹 Form-level validation (cross-field logic)
    def clean(self):
        cleaned_data = super().clean()
        order_type = cleaned_data.get('order_type')

        # Validate shipment fields if order_type == shipment
        if order_type == 'shipment':
            for field in ['shipping_address', 'shipping_city', 'shipping_state', 'shipping_zip']:
                if not cleaned_data.get(field):
                    self.add_error(field, "This field is required for shipment orders.")

        # Validate in-person (no need for shipping details)
        elif order_type == 'in_person':
            # You could clear them if accidentally filled
            cleaned_data['shipping_address'] = None
            cleaned_data['shipping_city'] = None
            cleaned_data['shipping_state'] = None
            cleaned_data['shipping_zip'] = None

        return cleaned_data

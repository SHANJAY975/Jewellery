from django.urls import reverse
from django.shortcuts import redirect

class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        
        # Check if user is authenticated
        if request.user.is_authenticated:
            paths_to_redirect = [reverse('SSJ:login'), reverse('SSJ:sign_up')]
            
            if request.path in paths_to_redirect:
                return redirect('SSJ:landing_page')
            
        response = self.get_response(request)
        return response
    

class RestrictUnauthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        restricted_paths = [reverse('SSJ:necklaces'),reverse('SSJ:logout'), reverse('SSJ:add_product'), reverse('SSJ:review_checkout'), reverse('SSJ:checkout'), reverse("SSJ:rings"), reverse("SSJ:all_products"), reverse("SSJ:bracelets"), reverse("SSJ:earrings"), reverse("SSJ:gold_rate"), reverse("SSJ:payment_success"), reverse("SSJ:verify_payment"), reverse("SSJ:generate_jewellery_image") ]
        
        if not request.user.is_authenticated:
            if request.path in restricted_paths:
                return redirect('SSJ:login')

        response = self.get_response(request)
        return response
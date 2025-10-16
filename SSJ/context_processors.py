# myapp/context_processors.py
from .models import Favourite, Cart, CartItem

def favourites(request):
    if request.user.is_authenticated:
        favs = Favourite.objects.filter(user=request.user).select_related('product')
    else:
        favs = []
    return {
        'favourites_list': favs
    }
    
def cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cartitems = CartItem.objects.filter(cart=cart).select_related("product")
    else:
        cartitems = []
    sub_total = 0
    for item in cartitems:
        price = item.product.current_price()
        sub_total += price
    gst = round((sub_total * 3)/100, 2)
    total = gst + sub_total
    return { 'cartitems': cartitems, 'sub_total':sub_total , "gst":gst, 'total':total}
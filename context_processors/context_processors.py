from cart.cart_module import Cart
from footer.models import ShopAddress
from product.models import Product, Favorite
from cart.models import Order, OrderItem
from account.models import Address
from django.views.generic import ListView


def cart_context(request):
    return {"cart": Cart(request)}

def get_address(request):
    return {'infos': ShopAddress.objects.all()}





# def get_context_data(request):
#     recent_orders = Order.objects.filter(user=request.user, is_paid=True)
#     favorites = Favorite.objects.filter(user=request.user)
#     return recent_orders, favorites
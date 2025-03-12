from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from product.models import Product
from account.models import User,Address
from .cart_module import Cart
from .models import Order, OrderItem, DiscountCode, UserDiscountCode
from django.conf import settings
import requests
import json

# Create your views here.

#######################################################
# my class based views
#######################################################
# def cart_detail(request):
#     cart = Cart(request)
#     return render(request, 'cart/cart_detail.html', {'cart': cart})

class AddToCartView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)

        selected_attributes = {}
        for key , value in request.POST.items():
            if key not in['csrfmiddlewaretoken', 'quantity']:
                selected_attributes[key] = value

        for attribute_name in selected_attributes.keys():
            selected_attributes.setdefault(attribute_name, 'N/A')

        quantity =  request.POST.get('quantity', 1)
        cart = Cart(request)
        cart.add(product, selected_attributes, quantity)


        return redirect('cart:cart_detail')


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        order, created = Order.objects.get_or_create(user=request.user ,is_paid=False)
        # order = get_object_or_404(Order, user=request.user)
        return render(request, 'cart/cart_detail.html', {'cart': cart, 'order': order})


#########################################################################
class RemoveFromCartView(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.delete(id)
        return redirect('cart:cart_detail')


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        cart = Cart(request)
        order = get_object_or_404(Order, id=id)
        return render(request, 'cart/order_detail.html', {'cart': cart,'order': order})


class CartToOrder(LoginRequiredMixin, View):
    def get(self, request, id):
        cart = Cart(request)
        # order, created = Order.objects.get_or_create(user=request.user,is_paid=False, total_price=cart.subtotal())
        order = Order.objects.filter(user=request.user, is_paid=False).first()
        if not order:
            order = Order.objects.create(user=request.user, is_paid=False)

        order.order_items.all().delete()

        for item in cart:
            order_item, created = OrderItem.objects.get_or_create(order=order, product=item['product'], attribute=item.get('attributes') ,quantity=item['quantity'],price=item['total'])

            if not created:
                order_item.price = int(item['total'])
                order_item.attribute.update(item.get('selected_attributes'))
                order_item.save()

        order.total_price = cart.order_grandtotal()
        order.item_quantities =  cart.product_quantity()
        order.save()

        # cart.remove_cart()
        return redirect('cart:order_detail', order.id)


# class AddressDetailView(LoginRequiredMixin, View):
#     def get(self, request):
#         order = Order.objects.get(user=request.user, is_paid=False)
#         return render(request, 'cart/addresses_detail.html', {'order': order})


class AddAddressToOrderView(LoginRequiredMixin, View):
    def post(self, request):
        order = Order.objects.get(user=request.user, is_paid=False)
        address = Address.objects.get(id=request.POST['selected_address'])
        order.address = address
        order.save()

        messages.success(request, 'آدرس شما انتخاب شد')
        return redirect('cart:order_detail', order.id)


class DiscountApplyView(View):
    def post(self, request, id):
        order = get_object_or_404(Order, id=id)
        code = request.POST.get('discount')
        discount_code = get_object_or_404(DiscountCode, code=code)
        discount_user = UserDiscountCode.objects.create(user=request.user, discount_code=discount_code)
        if discount_code.quantity == 0:
            return redirect('cart:order_detail', order.id)

        discount_price = (order.total_price * discount_code.discount)/100
        order.total_price -= discount_price
        order.save()
        discount_code.quantity -= 1
        discount_code.is_used = True
        discount_code.save()
        discount_user.overall_discount = discount_price
        discount_user.save()

        return redirect('cart:order_detail', order.id)

    def get(self, request, id):
        discount_price = UserDiscountCode.objects.get(overall_discount=request.user.overall_discount)
        return render(request, 'cart/order_detail.html', {'discount_price': discount_price })


class PurchaseOrderView(View):
    def post(self, request, id):
        order = get_object_or_404(Order, id=id)

        if order.address:
            order.is_paid = True
            order.save()
            return render(request, 'cart/success_purchase.html', {'order': order})

        else:
            messages.info(request, 'لطفا ابتدا ادرس خود را انتخاب کنید')
            return redirect('cart:order_detail', order.id)

# ? sandbox merchant
# if settings.SANDBOX:
#     sandbox = 'sandbox'
# else:
#     sandbox = 'www'
#
# ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
#
# amount = 1000  # Rial / Required
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# phone = '09214377940'  # Optional
# # Important: need to edit for realy server.
# CallbackURL = 'http://127.0.0.1:8000/verify/'
#
# class SendRequestView(View):
#     def post(self, request, pk):
#         order = get_object_or_404(Order, id=pk, user=request.user)
#         data = {
#             "MerchantID": settings.MERCHANT,
#             "Amount": order.total_price,
#             "Description": description,
#             "Phone": phone,
#             "CallbackURL": CallbackURL,
#         }
#         data = json.dumps(data)
#         # set content length by data
#         headers = {'content-type': 'application/json', 'content-length': str(len(data))}
#         try:
#             response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
#
#             if response.status_code == 200:
#                 response = response.json()
#                 if response['Status'] == 100:
#                     return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
#                             'authority': response['Authority']}
#                 else:
#                     return {'status': False, 'code': str(response['Status'])}
#             return response
#
#         except requests.exceptions.Timeout:
#             return {'status': False, 'code': 'timeout'}
#         except requests.exceptions.ConnectionError:
#             return {'status': False, 'code': 'connection error'}









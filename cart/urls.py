from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # path('cart', views.CartView.as_view(), name='cart_detail'),
    path('cart/detail/', views.CartDetailView.as_view(), name='cart_detail'),
    path('cart/add/<int:pk>', views.AddToCartView.as_view(), name='cart_add'),
    path('cart/delete/<str:id>', views.RemoveFromCartView.as_view(), name='cart_delete'),
    # path('cart/clear', views.clear_cart, name='clear_cart'),
    path('order/detail/<int:id>', views.OrderDetailView.as_view(), name='order_detail'),
    path('order/create/<int:id>', views.CartToOrder.as_view(), name='order_create'),
    path('address/add', views.AddAddressToOrderView.as_view(), name='add_address'),
    path('discount/apply/<int:id>', views.DiscountApplyView.as_view(), name='apply_discount'),
    path('purchase/<int:id>', views.PurchaseOrderView.as_view(), name='purchase_order'),
]

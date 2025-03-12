from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    # path('products',views.ProductListView.as_view(), name='product_list'),
    # path('detail/<int:pk>/<slug:slug>',views.ProductDetailView.as_view(), name='product_detail'),
    path('detail/<int:pk>/<slug:slug>',views.product_detail, name='product_detail'),
    path('navbar',views.NavbarPartialView.as_view(), name='navbar'),
    path('category/<slug:slug>',views.category_detail, name='category_detail'),
    path('category/<slug:category_slug>/<slug:subcategory_slug>',views.subcategory_detail, name='subcategory_detail'),
    path('offers',views.discounted_products, name='offers'),
    path('like/<int:id>', views.add_favorite, name='add_favorite'),
    path('remove/<int:id>', views.delete_favorite, name='remove_favorite'),
    path('favorites', views.favorite_list, name='favorite_list'),
    path('search/', views.search_products, name='search'),

]
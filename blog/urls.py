from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogHome.as_view(), name='home'),
    path('navbar',views.BlogNavbarPartialView.as_view(), name='navbar'),
    path('sidebar',views.SidebarPartialView.as_view(), name='sidebar'),
    path('signin/', views.UserLogin.as_view(), name='signin'),
    path('signout/', views.user_signout, name='signout'),
    path('search/', views.search_posts, name='search'),
    path('<slug:slug>', views.post_detail, name='post_detail'),
    path('<slug:category_slug>/', views.category_detail, name='category_list'),
    path('<slug:category_slug>/<slug:subcategory_slug>/', views.subcategory_detail, name='subcategory_list'),
    path('newposts', views.all_newposts, name='newposts'),
    path('like/<int:pk>/<slug:slug>/', views.like, name='like'),


]
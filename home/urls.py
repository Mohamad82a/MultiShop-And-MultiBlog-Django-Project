from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.Home.as_view(), name='main'),
    path('best_offers', views.best_offers_list, name='best_offers_list'),

]


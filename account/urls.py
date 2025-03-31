from django.urls import path
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView,  TokenRefreshView)


app_name = 'account'

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signin', views.UserLogin.as_view(), name='signin'),
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('registeration', views.registration, name='registeration'),
    path('profile/edit/<int:pk>', views.EditUserInfoView.as_view(), name='edit_profile'),
    path('code_check', views.CheckOtpView.as_view(), name='otp_check'),
    path('signout', views.user_signout, name='signout'),
    path('profile', views.UserPanelView.as_view(), name='user_profile'),
    path('profile/favorites', views.FavoritesInPanelView.as_view(), name='user_favorites'),
    path('profile/addresses', views.AddressesInPanelView.as_view(), name='user_addresses'),
    path('add/address', views.AddAddressView.as_view(), name='add_address'),
    path('addresse/edit/<int:pk>', views.EditAddressView.as_view(), name='edit_address'),
    path('addresse/delete/<int:pk>', views.DeleteAddressView.as_view(), name='delete_address'),
    path('profile/orders', views.OrdersView.as_view(), name='user_orders'),

]



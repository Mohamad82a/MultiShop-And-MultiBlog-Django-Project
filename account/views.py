from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView, DeleteView
from pyexpat.errors import messages

from .forms import LoginForm, RegisterForm, CheckOtpForm, AddressCreationForm, RegistrationForm, EditProfileForm
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
import ghasedak_sms
import ghasedakpack
from .models import Otp, User, Address
import os
from random import randint
from uuid import uuid4
from cart.models import Order, OrderItem
from product.models import Favorite

SMS = ghasedak_sms.Ghasedak('25628db02c16a6f2007d09e9f5551ebd5cf9a5661b9469b73e114d8a762f34ccEUTtdKQzTQZfGKB6')
# SMS = ghasedakpack.Ghasedak('25628db02c16a6f2007d09e9f5551ebd5cf9a5661b9469b73e114d8a762f34ccEUTtdKQzTQZfGKB6')


# Create your views here.

# def login(request):
#     return render(request, 'account/login.html', {})

class UserLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(username=cleaned_data['phone'], password=cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home:main')

            else:
                form.add_error('phone', 'شماره موبایل اشتباه است')
                form.add_error('password', 'رمزعبور اشتباه است')

        return render(request, 'account/login.html', {'form': form})


class SignUpView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            random_code = randint(10000, 99999)
            # SMS.verification({'receptor': cleaned_data['phone'], 'type': '1', 'template':'Ghasedak', 'param1':random_code})

            oldotp = ghasedak_sms.SendOldOtpInput(
                send_date='',
                receptors=[
                    ghasedak_sms.SendOtpReceptorDto(
                        mobile=cleaned_data['phone'],
                    )
                ],
                template_name='Ghasedak',
                param1=random_code,
                is_voice=False,
                udh=False
            )
            response = SMS.send_otp_sms_old(oldotp)
            print(response)
            print((random_code))

            token = str(uuid4)
            Otp.objects.create(phone=cleaned_data['phone'], code=random_code, token=token)

            return redirect(reverse('account:otp_check') + f'?token={token}')

        else:
            form.add_error('phone', 'شماره موبایل اشتباه است')

        return render(request, 'account/register.html', {'form': form})


class CheckOtpView(View):
    def get(self, request):
        form = CheckOtpForm()
        return render(request, 'account/otp_check.html', {'form': form})

    def post(self, request):
        form = CheckOtpForm(request.POST)
        token = request.GET.get('token')

        if form.is_valid():
            cleaned_data = form.cleaned_data
            if Otp.objects.filter(code=cleaned_data['code'], token=token).exists():
                otp = Otp.objects.get(token=token)
                user, is_created = User.objects.get_or_create(phone=otp.phone)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                otp.delete()
                return redirect('home:main')

        else:
            form.add_error('phone', 'کد تایید اشتباه است')

        phone_number = Otp.objects.filter(token=token).first().phone

        return render(request, 'account/otp_check.html', {'form': form, 'phone_number': phone_number})


from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import RegistrationForm  # اطمینان حاصل کنید که فرم را ایمپورت کرده‌اید

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone = form.cleaned_data.get('phone')

            messages.success(request, 'حساب کاربری شما با موفقیت ایجاد شد. \n اکنون میتوانید وارد حساب کاربری خود شوید')
            return redirect(reverse('home:main'))

        else:
            messages.error(request, 'ثبت ‌نام انجام نشد. لطفاً اطلاعات را بررسی کنید.')

    else:
        form = RegistrationForm()

    return render(request, 'account/registration.html', {'form': form})



class UserPanelView(TemplateView):
    template_name = 'account/user_panel.html'
    def get_context_data(self, **kwargs):
        context = super(UserPanelView, self).get_context_data(**kwargs)
        context['recent_orders'] = Order.objects.filter(user=self.request.user, is_paid=True).order_by('-order_date')
        context['user'] = self.request.user
        return context


class EditUserInfoView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'account/edit_userinfo.html'
    success_url = reverse_lazy('account:user_profile')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(EditUserInfoView, self).get_context_data(**kwargs)
        context['user'] = self.object
        return context


class OrdersView(UserPanelView):
    template_name = 'account/orders_panel.html'
    def get_context_data(self, **kwargs):
        context = super(OrdersView, self).get_context_data(**kwargs)
        context['user_orders'] = Order.objects.filter(user=self.request.user, is_paid=True).order_by('-order_date')
        return context


class FavoritesInPanelView(UserPanelView):
    template_name = 'account/favorites_panel.html'

    def get_context_data(self, **kwargs):
        context = super(FavoritesInPanelView, self).get_context_data(**kwargs)
        context['favorites'] = Favorite.objects.filter(user=self.request.user)
        return context

class AddressesInPanelView(UserPanelView):
    template_name = 'account/addresses_panel.html'

    def get_context_data(self, **kwargs):
        context = super(AddressesInPanelView, self).get_context_data(**kwargs)
        context['addresses'] = Address.objects.filter(user=self.request.user)
        return context


class AddAddressView(View):
    def post(self, request):
        form = AddressCreationForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()

            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)

        return render(request, 'account/add_address.html', {'form': form})

    def get(self, request):
        form = AddressCreationForm()
        return render(request, 'account/add_address.html', {'form': form})



class EditAddressView(UpdateView, UserPanelView):
    model = Address
    form_class = AddressCreationForm
    template_name = 'account/edit_address.html'
    success_url = reverse_lazy('account:user_addresses')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        if not hasattr(self, 'object'):
            self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        return context


class DeleteAddressView(DeleteView, UserPanelView):
    model = Address
    template_name = 'account/delete_address.html'
    success_url = reverse_lazy('account:panel_addresses')

    def get_context_data(self, **kwargs):
        if not hasattr(self, 'object'):
            self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        return context


def user_signout(request):
    logout(request)
    return redirect('home:main')



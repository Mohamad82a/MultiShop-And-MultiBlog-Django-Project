import jdatetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.migrations import serializer
from django.db.models import Q
from django.db.models.fields import return_None
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import localtime
from django.views import View
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

from account.forms import LoginForm
from account.models import User
from .serializers import UserSerializer, ArticleSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.views.generic import TemplateView, DetailView
import random
from.models import *
import bleach

# Create your views here.
class BlogNavbarPartialView(TemplateView):
    template_name = 'includes/blog_navbar.html'

    def get_context_data(self, **kwargs):
        context = super(BlogNavbarPartialView, self).get_context_data()
        context['categories'] = Category.objects.order_by('-id')
        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)



class SidebarPartialView(TemplateView):
    template_name = 'includes/blog_sidebar.html'

    def get_context_data(self, **kwargs):
        context = super(SidebarPartialView, self).get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.order_by('-date_published')[:3]
        context['categories'] = Category.objects.order_by('-id')
        return context


    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)




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
                return redirect('blog:home')

            else:
                form.add_error('phone', 'شماره موبایل اشتباه است')
                form.add_error('password', 'رمزعبور اشتباه است')

        return render(request, 'account/login.html', {'form': form})



class BlogHome(TemplateView):
    template_name = 'blog/home_blog.html'

    def get_context_data(self, **kwargs):
        context = super(BlogHome, self).get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.order_by('-date_published')[:10]
        # context['newest_posts'] = Post.objects.order_by('-date_published')
        newest_game_posts = list(Post.objects.filter(category__title='بازی').order_by('-date_published')[:10])
        context['newest_posts'] = random.sample(newest_game_posts, 5)
        context['categories'] = Category.objects.all()
        return context


def all_newposts(request):
    newest_game_posts = Post.objects.filter(category__title='بازی').order_by('-date_published')[:10]
    return render(request, 'blog/blog_list.html', {'newest_game_posts': newest_game_posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    last_updated = localtime(post.updated_at)
    jalali_date = jdatetime.datetime.fromgregorian(datetime=last_updated)
    persian_weekdays = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یک‌شنبه"]
    weekday_fa = persian_weekdays[jalali_date.weekday()]
    formatted_time = last_updated.strftime("%H:%M")

    if request.method == 'POST':
        parent_id = request.POST.get('parent_id')
        body = request.POST.get('body')
        Comment.objects.create(body=body, post=post, user=request.user, parent_id=parent_id)
        return redirect('blog:post_detail', slug=post.slug)


    is_liked = False
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        if user.likes.filter(post__slug=slug).exists():
            is_liked = True

        # else:
        #     is_liked = False

    return render(request, 'blog/post_detail.html', {'post': post, 'last_update': f"   {weekday_fa} ساعت {formatted_time}", 'is_liked': is_liked})



def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category)
    page_number = request.GET.get('page')
    paginator = Paginator(posts, 2)
    page_list = paginator.get_page(page_number)

    return render(request, 'blog/blog_list.html', {'posts': page_list, 'category': category})


def subcategory_detail(request, subcategory_slug, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    subcategory = Subcategory.objects.get(slug=subcategory_slug)
    posts = Post.objects.filter(category=category,subcategory=subcategory)
    page_number = request.GET.get('page')
    paginator = Paginator(posts, 2)
    page_list = paginator.get_page(page_number)

    return render(request, 'blog/blog_list.html', {'posts': page_list, 'subcategory': subcategory})


def search_posts(request):
    query = request.GET.get('search', '')
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(category__title__icontains=query) | Q(subcategory__title__icontains=query) | Q(body__icontains=query)
        )

    else:
        results = Post.objects.none()

    page_number = request.GET.get('page')
    paginator = Paginator(results, 2)
    page_list = paginator.get_page(page_number)

    return render(request, 'blog/blog_search_result.html', {'posts': page_list, 'query': query})

@login_required
def like(request, pk, slug):
    try:
        like = Like.objects.get(post__slug=slug, user_id=request.user.id)
        like.delete()
        return JsonResponse({'response': 'unliked'})

    except:
        Like.objects.create(post_id=pk, user_id=request.user.id)
        return JsonResponse({'response': 'liked'})



def user_signout(request):
    logout(request)
    return redirect('blog:home')
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from unicodedata import category
from product.models import Product,Category
from .models import HomeCarousel, UnderCarousel
from product.models import AttributeValue, Attribute
import random
from django.core.paginator import Paginator
# Create your views here.


class Home(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['mobiles'] = Product.objects.filter(subcategory__title='برند های مختلف گوشی')
        context['categories'] = Category.objects.all()
        context['best_offers'] = Product.objects.filter(discount_percentage__gt=3)
        context['offers'] = HomeCarousel.objects.all()
        context['side_offers'] = UnderCarousel.objects.all()
        return context



def best_offers_list(request):
    products = Product.objects.filter(discount_percentage__gt=3)

    color_values = AttributeValue.objects.filter(attribute__name='رنگ', product__in=products)
    size_values = AttributeValue.objects.filter(attribute__name='سایز', product__in=products)
    measure_values = AttributeValue.objects.filter(attribute__name='اندازه', product__in=products)

    temp_colors = set()
    unique_colors = {}
    for value in color_values:
        if value.value not in temp_colors:
            temp_colors.add(value.value)
            if value.attribute not in unique_colors:
                unique_colors[value.attribute] = []

            unique_colors[value.attribute].append(value.value)

    temp_sizes = set()
    unique_sizes = {}
    for value in size_values:
        if value.value not in temp_sizes:
            temp_sizes.add(value.value)
            if value.attribute not in unique_sizes:
                unique_sizes[value.attribute] = []

            unique_sizes[value.attribute].append(value.value)


    temp_measures = set()
    unique_measures = {}
    for value in measure_values:
        if value.value not in temp_measures:
            temp_measures.add(value.value)
            if value.attribute not in unique_measures:
                unique_measures[value.attribute] = []

            unique_measures[value.attribute].append(value.value)

    min_price = request.GET.get('min_price', 0)
    max_price = request.GET.get('max_price', 0)
    colors = request.GET.getlist('color')
    sizes = request.GET.getlist('size')
    measures = request.GET.getlist('measure')

    if min_price and max_price:
        products = Product.objects.filter(discount_percentage__gt=3, price__gte=min_price, price__lte=max_price)

    if colors:
        color_products = AttributeValue.objects.filter(attribute__name='رنگ', value__in=colors).values_list('product',
                                                                                                            flat=True)
        products = products.filter(discount_percentage__gt=3, id__in=list(color_products))

    if sizes:
        size_products = AttributeValue.objects.filter(attribute__name='سایز', value__in=sizes).values_list('product',
                                                                                                           flat=True)
        products = products.filter(discount_percentage__gt=3, id__in=list(size_products))

    if measures:
        measure_products = AttributeValue.objects.filter(attribute__name='اندازه', value__in=measures).values_list(
            'product', flat=True)
        products = products.filter(category=category, id__in=list(measure_products))


    products = products.distinct()

    for product in products:
        product.update_discount()

    search_query = request.GET.get('q', '')
    sorting_option = request.GET.get('sort', '')

    if search_query:
        products = products.filter(name__contains=search_query)

    if sorting_option == 'بالا ترین':
        products = products.order_by('-price')

    elif sorting_option == 'کم ترین':
        products = products.order_by('price')

    elif sorting_option == 'جدید ترین':
        products = products.order_by('-created')

    items_per_page = request.GET.get('items_per_page', 3)

    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page', 1)
    page_list = paginator.get_page(page_number)

    return render(request, 'product/best_offers_list.html', {
        'products': page_list,
        'category': category,
        'pages': page_list,
        'sorting_option': sorting_option,
        'search_query': search_query,
        'unique_colors': unique_colors,
        'unique_sizes': unique_sizes,
        'unique_measures': unique_measures,
        'selected_colors': colors,
        'selected_sizes': sizes,
        'selected_measures': measures,
    })


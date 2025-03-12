from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from unicodedata import category

from product.models import Product, Category, Favorite, Subcategory, Attribute, AttributeValue
from django.views.generic import DetailView, TemplateView,ListView, View
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.


# class ProductDetailView(DetailView):
#     model = Product
#     template_name = 'product/product_detail.html'

def product_detail(request, pk, slug):
    product = Product.objects.get( pk=pk, slug=slug)
    attributes = AttributeValue.objects.filter(product=product)

    grouped_attributes = {}
    for attribute in attributes:
        if attribute.attribute.name not in grouped_attributes:
            grouped_attributes[attribute.attribute.name] = []
        grouped_attributes[attribute.attribute.name].append(attribute.value)



    return render(request, 'product/product_detail.html', {'product': product, 'grouped_attributes': grouped_attributes})


class NavbarPartialView(TemplateView):
    template_name = 'includes/navbar.html'

    def get_context_data(self, **kwargs):
        context = super(NavbarPartialView, self).get_context_data()
        context['categories'] = Category.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

#class based view

# class CategoryDateilView(ListView):
#     template_name = 'product/category_detail.html'
#     context_object_name1 = 'products'
#     paginate_by = 2
#
#
#     def get_queryset(self):
#         slug = self.kwargs['slug']
#         return Product.objects.filter(category__slug=slug)
#
#     def get_context_data(self, **kwargs):
#         context = super(CategoryDateilView, self).get_context_data()
#         category = get_object_or_404(Category, slug=self.kwargs['slug'])
#         context['category'] = category
#         context['products'] = Product.objects.filter(category=category)
#         return context



#function based view

def category_detail(request,slug):
    # pk = pk.replace('-',' ')

    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category)

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
        products = Product.objects.filter(category=category,price__gte=min_price, price__lte=max_price)



    if colors:
        color_products = AttributeValue.objects.filter(attribute__name='رنگ', value__in=colors).values_list('product',flat=True)
        products = products.filter(category=category,id__in=list(color_products))

    if sizes:
        size_products = AttributeValue.objects.filter(attribute__name='سایز', value__in=sizes).values_list('product', flat=True)
        products = products.filter(category=category,id__in=list(size_products))

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
        products = products.filter(name__contains = search_query)

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

    return render(request, 'product/category_detail.html', {
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


def subcategory_detail(request, category_slug, subcategory_slug):
    # pk = pk.replace('-',' ')

    category = Category.objects.get(slug=category_slug)
    subcategory = Subcategory.objects.get(slug=subcategory_slug)
    products = Product.objects.filter(subcategory=subcategory)

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
        products = Product.objects.filter(category=category,price__gte=min_price, price__lte=max_price)



    if colors:
        color_products = AttributeValue.objects.filter(attribute__name='رنگ', value__in=colors).values_list('product',flat=True)
        products = products.filter(category=category,id__in=list(color_products))

    if sizes:
        size_products = AttributeValue.objects.filter(attribute__name='سایز', value__in=sizes).values_list('product', flat=True)
        products = products.filter(category=category,id__in=list(size_products))

    if measures:
        measure_products = AttributeValue.objects.filter(attribute__name='اندازه', value__in=measures).values_list(
            'product', flat=True)
        products = products.filter(category=category, id__in=list(measure_products))

    products = products.distinct()

    search_query = request.GET.get('q', '')
    sorting_option = request.GET.get('sort', '')

    if search_query:
        products = products.filter(name__contains = search_query)

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



    return render(request, 'product/category_detail.html', {
        'products': page_list,
        'category': category,
        'subcategory': subcategory,
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

def discounted_products(request):
    # pk = pk.replace('-',' ')
    products = Product.objects.filter(discount__gt=0)
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
        products = Product.objects.filter(category=category,price__gte=min_price, price__lte=max_price)



    if colors:
        color_products = AttributeValue.objects.filter(attribute__name='رنگ', value__in=colors).values_list('product',flat=True)
        products = products.filter(category=category,id__in=list(color_products))

    if sizes:
        size_products = AttributeValue.objects.filter(attribute__name='سایز', value__in=sizes).values_list('product', flat=True)
        products = products.filter(category=category,id__in=list(size_products))

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
        products = products.filter(name__contains = search_query)

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



    return render(request, 'product/product_offers.html', {
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

# add to favorite
@login_required
def add_favorite(request, id):
    favorite_product = get_object_or_404(Product, id=id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=favorite_product)
    if created:
        messages.success(request,'محصول به لیست علاقه مندی ها اضافه شد')

    else:
        messages.info(request, 'محصول در لیست علاقه مندی شما قرار دارد')


    return redirect(request.META.get('HTTP_REFERER', 'product:category_detail'))



@login_required
def delete_favorite(request, id):
    product = get_object_or_404(Product, id=id)
    Favorite.objects.filter(user=request.user, product=product).delete()
    return redirect('product:favorite_list')

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'product/favorite_list.html', {'favorites': favorites})



def search_products(request):
    query = request.GET.get('search', '')
    if query:
        results = Product.objects.filter(
            Q(title__icontains=query) | Q(category__title__icontains=query) | Q(subcategory__title__icontains=query)
        )
    else:
        results = Product.objects.none()

    color_values = AttributeValue.objects.filter(attribute__name='رنگ', product__in=results)
    size_values = AttributeValue.objects.filter(attribute__name='سایز', product__in=results)
    measure_values = AttributeValue.objects.filter(attribute__name='اندازه', product__in=results)

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
        results = results.filter(price__gte=min_price, price__lte=max_price)

    if colors:
        color_products = AttributeValue.objects.filter(attribute__name='رنگ', value__in=colors).values_list(
            'product', flat=True)
        results = results.filter(id__in=list(color_products))

    if sizes:
        size_products = AttributeValue.objects.filter(attribute__name='سایز', value__in=sizes).values_list(
            'product', flat=True)
        results = results.filter(id__in=list(size_products))

    if measures:
        measure_products = AttributeValue.objects.filter(attribute__name='اندازه', value__in=measures).values_list(
            'product', flat=True)
        results = results.filter(id__in=list(measure_products))

    results = results.distinct()

    for product in results:
        product.update_discount()

    search_query = request.GET.get('q', '')
    sorting_option = request.GET.get('sort', '')

    if search_query:
        results = results.filter(name__icontains=search_query)

    if sorting_option == 'بالا ترین':
        results = results.order_by('-price')

    elif sorting_option == 'کم ترین':
        results = results.order_by('price')

    elif sorting_option == 'جدید ترین':
        results = results.order_by('-created')

    items_per_page = int(request.GET.get('items_per_page', 3))

    paginator = Paginator(results, items_per_page)
    page_number = request.GET.get('page', 1)
    page_list = paginator.get_page(page_number)

    return render(request, 'product/search_result.html', {
        'products': page_list,
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
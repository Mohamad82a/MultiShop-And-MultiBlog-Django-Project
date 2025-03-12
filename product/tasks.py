from celery import shared_task
from product.models import Product
from django.utils import timezone

@shared_task
def remove_expired_discounts():
    expired_discounts = Product.objects.filter(discount_expiry__lte = timezone.now())
    for product in expired_discounts:
        product.remove_discount()
# Generated by Django 5.1.5 on 2025-02-18 10:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0031_remove_product_category_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.category', verbose_name='دسته بندی محصول'),
        ),
    ]

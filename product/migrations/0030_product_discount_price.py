# Generated by Django 5.1.5 on 2025-02-17 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0029_alter_product_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_price',
            field=models.BigIntegerField(default=0),
        ),
    ]

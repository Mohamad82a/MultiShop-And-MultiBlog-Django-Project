# Generated by Django 5.1.5 on 2025-03-06 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_address_options_user_melicode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='melicode',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='کد ملی'),
        ),
    ]

# Generated by Django 5.1.5 on 2025-02-26 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnderCarousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_title', models.CharField(max_length=100, verbose_name='نام عکس')),
                ('image', models.ImageField(upload_to='homecarousel', verbose_name='عکس')),
            ],
            options={
                'verbose_name': 'عکس جانبی صفحه',
                'verbose_name_plural': 'عکس های جانبی صفحه',
            },
        ),
    ]

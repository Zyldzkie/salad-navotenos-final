# Generated by Django 5.0.4 on 2024-05-11 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_order_shipping_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='profile_image',
        ),
    ]

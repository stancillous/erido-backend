# Generated by Django 5.0.1 on 2024-02-01 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eridosolutions', '0003_alter_shoppingcart_user_alter_address_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='eridosolutions/product_images/'),
        ),
    ]

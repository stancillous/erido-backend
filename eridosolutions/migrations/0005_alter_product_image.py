# Generated by Django 5.0.1 on 2024-02-01 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eridosolutions', '0004_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]

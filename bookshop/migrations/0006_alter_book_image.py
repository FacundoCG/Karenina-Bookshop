# Generated by Django 3.2.12 on 2023-07-09 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0005_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(upload_to='bookshop', verbose_name='Imagen'),
        ),
    ]

# Generated by Django 5.0.6 on 2024-07-12 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='', upload_to='img/'),
            preserve_default=False,
        ),
    ]
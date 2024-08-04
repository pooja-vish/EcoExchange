# Generated by Django 5.0.6 on 2024-08-03 19:46

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_details', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_bid', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('current_winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_details.member')),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='product.auction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_details.member')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=255)),
                ('product_description', models.TextField()),
                ('image', models.ImageField(upload_to='img/')),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('price', models.IntegerField()),
                ('category', models.CharField(choices=[('PAPER', 'Paper'), ('PLASTIC', 'Plastic'), ('GLASS', 'Glass'), ('METAL', 'Metal'), ('ELECTRONICS', 'Electronics'), ('ORGANIC', 'Organic'), ('TEXTILES', 'Textiles'), ('BATTERIES', 'Batteries'), ('WOOD', 'Wood'), ('RUBBER', 'Rubber'), ('MIXED_MATERIALS', 'Mixed Materials')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_details.member')),
            ],
        ),
        migrations.AddField(
            model_name='auction',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
        migrations.CreateModel(
            name='Queries',
            fields=[
                ('choices', models.CharField(choices=[('Account_Management', 'Account Management'), ('Technical_issues', 'Technical issues'), ('Billing_payments', 'Billing & Payments'), ('Product_service', 'Product Service Information'), ('Other', 'Other')], max_length=50)),
                ('description', models.TextField()),
                ('ticket_id', models.IntegerField(primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_details.member')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('is_available', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_details.member')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='product.product')),
            ],
            options={
                'unique_together': {('user', 'product')},
            },
        ),
    ]

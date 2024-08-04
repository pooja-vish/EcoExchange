# Generated by Django 5.0.6 on 2024-08-03 19:46

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_details', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_date', models.DateField(default=django.utils.timezone.now)),
                ('order_amount', models.IntegerField()),
                ('order_status', models.CharField(choices=[('P', 'Pending'), ('S', 'Shipped'), ('D', 'Delivered'), ('C', 'Cancelled')], default='P', max_length=1)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_details.member')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
        ),
    ]

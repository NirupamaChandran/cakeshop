# Generated by Django 5.0.1 on 2024-03-15 06:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_basketitem_occasion_object'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basketitem',
            name='cake_varient_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cakevarient', to='shop.cake'),
        ),
    ]

# Generated by Django 5.0.1 on 2024-03-30 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_orderitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customization',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]

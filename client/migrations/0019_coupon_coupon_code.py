# Generated by Django 4.0.1 on 2022-03-24 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0018_coupon_sales'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='coupon_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]

# Generated by Django 4.0.1 on 2022-06-20 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0044_onetoonemessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactuser',
            name='sales',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
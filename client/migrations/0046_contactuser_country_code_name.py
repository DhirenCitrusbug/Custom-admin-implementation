# Generated by Django 4.0.1 on 2022-07-20 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0045_alter_contactuser_sales'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactuser',
            name='country_code_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
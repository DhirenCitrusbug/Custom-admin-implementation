# Generated by Django 3.2.12 on 2022-05-10 05:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20220509_1829'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trustedaccessories',
            old_name='Placements',
            new_name='placements',
        ),
    ]
# Generated by Django 4.0.1 on 2022-10-04 05:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aegency_user', '0007_alter_agencyhostname_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agencyuser',
            options={'verbose_name': 'Agency User', 'verbose_name_plural': 'Agency Users'},
        ),
    ]
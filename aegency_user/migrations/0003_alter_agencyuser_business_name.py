# Generated by Django 4.0.1 on 2022-02-23 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aegency_user', '0002_rename_aegencyuser_agencyuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agencyuser',
            name='business_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]

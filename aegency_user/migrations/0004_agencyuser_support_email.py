# Generated by Django 4.0.1 on 2022-06-27 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aegency_user', '0003_alter_agencyuser_business_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='agencyuser',
            name='support_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]

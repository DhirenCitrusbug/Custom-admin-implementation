# Generated by Django 4.0.1 on 2022-05-25 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0040_customfields_field_placeholder'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacttocampaign',
            name='is_last',
            field=models.BooleanField(default=False),
        ),
    ]

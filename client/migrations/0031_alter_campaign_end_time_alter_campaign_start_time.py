# Generated by Django 4.0.1 on 2022-04-19 09:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0030_campaign_on_cancel_keyword_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='end_time',
            field=models.TimeField(default=datetime.time(20, 0)),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='start_time',
            field=models.TimeField(default=datetime.time(8, 0)),
        ),
    ]

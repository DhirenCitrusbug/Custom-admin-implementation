# Generated by Django 4.0.1 on 2022-04-21 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0031_alter_campaign_end_time_alter_campaign_start_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='cancel_tag',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='on_cancel_keyword',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='on_cancel_message',
        ),
        migrations.AlterField(
            model_name='campaignaction',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
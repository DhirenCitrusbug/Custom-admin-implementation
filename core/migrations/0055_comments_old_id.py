# Generated by Django 3.2.12 on 2022-08-10 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0054_auto_20220810_0447'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='old_id',
            field=models.IntegerField(default=0),
        ),
    ]

# Generated by Django 4.0.2 on 2022-02-15 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='is_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='client',
            name='server_passcode',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

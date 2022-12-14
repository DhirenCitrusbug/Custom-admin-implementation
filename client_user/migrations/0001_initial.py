# Generated by Django 4.0.2 on 2022-02-14 15:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_user', '0006_alter_address_address'),
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientUser',
            fields=[
                ('admin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('account_sid', models.CharField(blank=True, max_length=100, null=True)),
                ('auth_token', models.TextField(blank=True, null=True)),
                ('server_passcode', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_user.address')),
                ('client_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_owner', to='client.client')),
            ],
            options={
                'abstract': False,
            },
            bases=('admin_user.admin',),
        ),
    ]

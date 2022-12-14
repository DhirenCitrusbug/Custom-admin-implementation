# Generated by Django 4.0.1 on 2022-03-15 12:26

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('admin_user', '0008_admin_is_forget_alter_admin_first_name_and_more'),
        ('client', '0008_contactlist_list_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientPhoneNumber',
            fields=[
                ('activitytracking_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='admin_user.activitytracking')),
                ('name', models.CharField(max_length=30)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('is_default', models.BooleanField(default=True)),
                ('phone_sid', models.CharField(blank=True, max_length=30, null=True)),
                ('phone_type', models.CharField(blank=True, max_length=10, null=True)),
                ('client_phone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='client.client')),
            ],
            bases=('admin_user.activitytracking',),
        ),
    ]

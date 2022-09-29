# Generated by Django 3.2.12 on 2022-03-23 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_user', '0009_alter_timezone_name'),
        ('client', '0015_broadcast_is_sent_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('activitytracking_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='admin_user.activitytracking')),
                ('coupon_name', models.CharField(blank=True, max_length=30, null=True)),
                ('discount_type', models.CharField(blank=True, max_length=30, null=True)),
                ('discount_value', models.IntegerField(blank=True, null=True)),
                ('minmum_spend', models.IntegerField(blank=True, null=True)),
                ('valid_from', models.DateTimeField(blank=True, null=True)),
                ('valid_to', models.DateTimeField(blank=True, null=True)),
                ('is_read_count', models.IntegerField(blank=True, null=True)),
                ('is_valid', models.BooleanField(default=True)),
                ('is_no_end', models.BooleanField(default=False)),
            ],
            bases=('admin_user.activitytracking',),
        ),
    ]
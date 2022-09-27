# Generated by Django 4.0.1 on 2022-02-07 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_user', '0004_country_state_alter_address_country_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeZone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=3, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='admin',
            name='time_zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_user.timezone'),
        ),
    ]
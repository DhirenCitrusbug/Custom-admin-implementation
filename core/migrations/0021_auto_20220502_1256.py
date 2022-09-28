# Generated by Django 3.2.12 on 2022-05-02 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_pages_meta_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='pages',
            name='bike_class',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='pages',
            name='brands',
            field=models.ManyToManyField(db_index=True, related_name='pages_brand', to='core.ReviewBrand'),
        ),
        migrations.AddField(
            model_name='pages',
            name='categories',
            field=models.ManyToManyField(db_index=True, related_name='pages_category', to='core.ReviewCategory'),
        ),
        migrations.AddField(
            model_name='pages',
            name='filter_type',
            field=models.BooleanField(choices=[(True, 'Basic search filter'), (False, 'Advanced search filter')], default='True'),
        ),
        migrations.AddField(
            model_name='pages',
            name='max_battery_capacity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pages',
            name='max_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pages',
            name='max_weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pages',
            name='max_year',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='pages',
            name='min_battery_capacity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pages',
            name='min_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pages',
            name='min_weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pages',
            name='min_year',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='pages',
            name='motor_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='pages',
            name='suspension',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

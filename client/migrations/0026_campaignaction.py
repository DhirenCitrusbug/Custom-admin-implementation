# Generated by Django 4.0.1 on 2022-04-13 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_user', '0009_alter_timezone_name'),
        ('client', '0025_days_keyword_campaign'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignAction',
            fields=[
                ('activitytracking_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='admin_user.activitytracking')),
                ('action', models.JSONField(blank=True, null=True)),
                ('order', models.IntegerField()),
                ('campaign_action', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='client.campaign')),
            ],
            options={
                'unique_together': {('campaign_action', 'order')},
            },
            bases=('admin_user.activitytracking',),
        ),
    ]

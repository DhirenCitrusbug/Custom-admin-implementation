# Generated by Django 4.0.1 on 2022-08-09 05:23

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('admin_user', '0010_timezone_value'),
        ('client', '0049_contactusercoupon_second_message_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='is_referral_dis',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='coupon',
            name='is_referral_reward',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='ReferralRewardCouponContactUser',
            fields=[
                ('activitytracking_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='admin_user.activitytracking')),
                ('amount', models.FloatField(blank=True, null=True)),
                ('is_read', models.BooleanField(default=False)),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('new_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='new_contact_user', to='client.contactuser')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='old_contact_user', to='client.contactuser')),
                ('user_coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='client.coupon')),
            ],
            options={
                'unique_together': {('user', 'new_user')},
            },
            bases=('admin_user.activitytracking',),
        ),
    ]
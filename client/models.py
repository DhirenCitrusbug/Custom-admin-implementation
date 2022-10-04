import datetime
import random
import string
from http import client
import uuid

from django.db import models
from admin_user.models import Admin,Address,ActivityTracking,TimeZone
from aegency_user.models import AgencyUser
# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField

class Client(Admin):
    business_name=models.CharField(max_length=30,blank=True,null=True)
    business_email=models.EmailField(blank=True,null=True)
    business_phone_no=models.CharField(max_length=15,blank=True,null=True)
    account_sid=models.CharField(max_length=100,blank=True,null=True)
    auth_token=models.TextField(blank=True,null=True)
    aegency=models.ForeignKey(AgencyUser,on_delete=models.CASCADE,related_name='agency_user')
    address=models.ForeignKey(Address,on_delete=models.SET_NULL,blank=True,null=True)
    is_user=models.BooleanField(default=False)
    server_passcode=models.CharField(max_length=50,blank=True,null=True)
    message_service_id=models.CharField(max_length=128,blank=True,null=True)

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):

        super().save(*args, *kwargs)
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

class Tags(ActivityTracking):
    name=models.CharField(max_length=30)
    client_tag=models.ForeignKey(Client,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.name


class ClientPhoneNumber(ActivityTracking):
    name=models.CharField(max_length=30)
    client_phone=models.ForeignKey(Client,on_delete=models.CASCADE,blank=True,null=True)
    phone_number=PhoneNumberField(blank=True,null=True)
    is_default=models.BooleanField(default=False)
    phone_sid = models.CharField(max_length=128,blank=True,null=True)
    phone_type = models.CharField(max_length=10,blank=True,null=True)
    phone_message_service_id=models.CharField(max_length=128,blank=True,null=True)

    def __str__(self):
        return self.name


class Coupon(ActivityTracking):
    coupon_name = models.CharField(max_length=30,blank=True,null=True)
    discount_type = models.CharField(max_length=30,blank=True,null=True)
    discount_value = models.FloatField(blank=True,null=True)
    minmum_spend = models.FloatField(blank=True,null=True)
    valid_from = models.DateTimeField(blank=True,null=True)
    valid_to = models.DateTimeField(blank=True,null=True)
    is_read_count= models.IntegerField(blank=True,null=True)
    max_read_count= models.IntegerField(blank=True,null=True)
    is_valid=models.BooleanField(default=True)
    is_no_end=models.BooleanField(default=False)
    client_coupon=models.ForeignKey(Client,on_delete=models.CASCADE,blank=True,null=True)
    sales=models.FloatField(blank=True,null=True)
    coupon_code=models.CharField(max_length=20,blank=True,null=True)
    is_referral=models.BooleanField(default=False)
    is_referral_reward=models.BooleanField(default=False)
    is_referral_dis=models.BooleanField(default=False)


    def __str__(self):
        return self.coupon_name


class Keyword(ActivityTracking):
    name=models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Days(ActivityTracking):
    name=models.CharField(max_length=30)
    is_defualt=models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Campaign(ActivityTracking):
    name=models.CharField(max_length=30,blank=True,null=True)
    keyword_phone=models.ForeignKey(ClientPhoneNumber,related_name='keyword_phone',on_delete=models.CASCADE,blank=True,null=True)
    keyword_value=models.CharField(max_length=30,blank=True,null=True)
    is_sending=models.BooleanField(default=True)
    sending_days=models.ManyToManyField(Days,blank=True,null=True)
    start_time=models.TimeField(default=datetime.time(8, 00))
    end_time=models.TimeField(default=datetime.time(20, 00))
    send_phone=models.ForeignKey(ClientPhoneNumber,related_name='send_phone',on_delete=models.CASCADE,blank=True,null=True)
    is_double=models.BooleanField(default=False)
    double_keyword=models.CharField(max_length=30,blank=True,null=True)
    double_message=models.TextField(blank=True,null=True)
    is_limit=models.BooleanField(default=False)
    limit_message = models.TextField(blank=True, null=True)
    in_progress_count=models.IntegerField(default=0)
    complate_count=models.IntegerField(default=0)
    steps=models.IntegerField(default=0)
    is_cancel=models.BooleanField(default=False)
    on_reply=models.BooleanField(default=False)
    is_cancel_tag=models.BooleanField(default=False)
    trigger_type=models.JSONField(blank=True,null=True)
    client_campaign=models.ForeignKey(Client,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.name


class CampaignAction(ActivityTracking):
    campaign_action=models.ForeignKey(Campaign,on_delete=models.CASCADE,blank=True,null=True)
    action=models.JSONField(blank=True,null=True)
    order=models.IntegerField(blank=True,null=True)


class ContactUser(ActivityTracking):
    phone_no=PhoneNumberField(blank=True,null=True)
    country_code_name=models.CharField(max_length=50,blank=True,null=True)
    first_name=models.CharField(max_length=15,blank=True,null=True)
    last_name=models.CharField(max_length=15,blank=True,null=True)
    birthday=models.DateField(blank=True,null=True)
    anniversary=models.DateField(blank=True,null=True)
    tags=models.ManyToManyField(Tags,blank=True,null=True)
    time_zone=models.ForeignKey(TimeZone,on_delete=models.SET_NULL,blank=True,null=True)
    client=models.ForeignKey(Client,on_delete=models.SET_NULL,blank=True,null=True)
    sales=models.FloatField(blank=True,null=True,default=0)
    is_active=models.BooleanField(default=True)
    active_campaign=models.ManyToManyField(Campaign,blank=True,null=True)


class ContactList(ActivityTracking):
    name=models.CharField(max_length=30)
    contacts=models.ManyToManyField(ContactUser)
    is_static=models.BooleanField(default=False)
    is_smart=models.BooleanField(default=False)
    list_owner=models.ForeignKey(Client,on_delete=models.CASCADE,blank=True,null=True)
    rev_type=models.CharField(max_length=30,blank=True,null=True)
    rev_val=models.IntegerField(blank=True,null=True)
    rev_from=models.IntegerField(blank=True,null=True)
    rev_to=models.IntegerField(blank=True,null=True)
    date_type = models.CharField(max_length=30, blank=True, null=True)
    date_val=models.DateField(blank=True,null=True)
    date_from=models.DateField(blank=True,null=True)
    date_to=models.DateField(blank=True,null=True)

    def __str__(self):
        return self.name


class BroadCast(ActivityTracking):
    message=models.TextField()
    contacts=models.ManyToManyField(ContactUser,blank=True,null=True)
    contact_list=models.ManyToManyField(ContactList,blank=True,null=True)
    is_sent=models.BooleanField(default=False)
    is_schdeule=models.BooleanField(default=False)
    sch_date=models.DateTimeField(blank=True,null=True)
    client_brodcast=models.ForeignKey(Client,on_delete=models.CASCADE,blank=True,null=True)
    contacts_count=models.IntegerField(blank=True,null=True)
    is_sent_count=models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.message


class ContactUserCoupon(ActivityTracking):

    user=models.ForeignKey(ContactUser,on_delete=models.CASCADE,blank=True,null=True)
    user_coupon=models.ForeignKey(Coupon,on_delete=models.CASCADE,blank=True,null=True)
    is_read=models.BooleanField(default=False)
    unique_id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    short_url=models.CharField(max_length=10,blank=True,null=True)
    amount=models.FloatField(blank=True,null=True)
    second_message_sent=models.BooleanField(default=False)

    class Meta:
        unique_together = ('user','user_coupon')

    def save(self, *args, **kwargs):
        if not self.short_url:
            url = ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=8))
            url=get_unique_shourt_url(url)
            self.short_url=url
        super(ContactUserCoupon, self).save()


class ContactToCampaign(ActivityTracking):
    campaign_action=models.ForeignKey(CampaignAction,on_delete=models.CASCADE,blank=True,null=True)
    contact_user=models.ForeignKey(ContactUser,on_delete=models.CASCADE,blank=True,null=True)
    is_true=models.BooleanField(default=False)
    date_time=models.DateTimeField(blank=True,null=True)
    type=models.JSONField(blank=True,null=True)
    is_last=models.BooleanField(default=False)


class CustomFields(ActivityTracking):
    field_name=models.CharField(max_length=30,blank=True,null=True)
    field_placeholder=models.CharField(max_length=100,blank=True,null=True)
    field_type=models.CharField(max_length=30,blank=True,null=True)
    client_field=models.ForeignKey(Client,on_delete=models.CASCADE,blank=True,null=True)

class CustomFieldsValue(ActivityTracking):
    field_value=models.TextField(blank=True,null=True)
    custom_field=models.ForeignKey(CustomFields,on_delete=models.CASCADE,blank=True,null=True)
    contact_user=models.ForeignKey(ContactUser,on_delete=models.CASCADE,blank=True,null=True)

class DoubleOptinCampaign(ActivityTracking):
    contact_user=models.ForeignKey(ContactUser,on_delete=models.CASCADE,blank=True,null=True)
    campagin=models.ForeignKey(Campaign,on_delete=models.CASCADE,blank=True,null=True)

class OneToOneMessage(ActivityTracking):
    message=models.TextField()
    contact=models.ForeignKey(ContactUser,on_delete=models.CASCADE,blank=True,null=True)
    client=models.ForeignKey(Client,on_delete=models.CASCADE,blank=True,null=True)
    is_send=models.BooleanField(default=False)
    is_receive=models.BooleanField(default=False)

class ReferralCampaigns(ActivityTracking):
    ref_camp_name = models.CharField(max_length=30,blank=True,null=True)
    ref_coupon = models.ForeignKey(Coupon,related_name='referral_coupon',on_delete=models.CASCADE,blank=True,null=True)
    reward_coupon = models.ForeignKey(Coupon,related_name='reward_coupon',on_delete=models.CASCADE,blank=True,null=True)
    is_read_count= models.IntegerField(blank=True,null=True)
    max_read_count= models.IntegerField(blank=True,null=True)
    client_rc=models.ForeignKey(Client,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.ref_camp_name

class ReferralCampaignToContact(ActivityTracking):
    referral_camp = models.ForeignKey(ReferralCampaigns,on_delete=models.CASCADE,blank=True,null=True)
    contact_user = models.ForeignKey(ContactUser,related_name='contact_user',on_delete=models.CASCADE,blank=True,null=True)
    refered_user = models.ManyToManyField(ContactUser,related_name='refered_user',blank=True,null=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_added = models.BooleanField(default=False)
    short_url = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        unique_together = ('referral_camp','contact_user')

    def save(self, *args, **kwargs):
        if not self.short_url:
            url = ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=8))
            url=get_unique_reward_shourt_url(url)
            self.short_url=url
        super(ReferralCampaignToContact, self).save()


class ReferralRewardCouponContactUser(ActivityTracking):
    user = models.ForeignKey(ContactUser,related_name='old_contact_user',on_delete=models.CASCADE,blank=True,null=True)
    new_user = models.ForeignKey(ContactUser,related_name='new_contact_user',on_delete=models.CASCADE,blank=True,null=True)
    user_coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE,blank=True,null=True)
    amount=models.FloatField(blank=True,null=True)
    is_read=models.BooleanField(default=False)
    unique_id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    short_url = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        unique_together = ('user','new_user')

    def save(self, *args, **kwargs):
        if not self.short_url:
            url = ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=8))
            url=get_unique_shourt_url(url)
            self.short_url=url
        super(ReferralRewardCouponContactUser, self).save()


def get_unique_shourt_url(short_url):
    shourt_url1 = ReferralRewardCouponContactUser.objects.filter(short_url=short_url).distinct()
    shourt_url2 = ContactUserCoupon.objects.filter(short_url=short_url).distinct()
    if shourt_url1.exists() or shourt_url2.exists():
        a = ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=8))
        return get_unique_shourt_url(a)
    return short_url

def get_unique_reward_shourt_url(short_url):
    shourt_url = ReferralCampaignToContact.objects.filter(short_url=short_url).distinct()
    if shourt_url.exists():
        a = ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=8))
        return get_unique_shourt_url(a)
    return short_url
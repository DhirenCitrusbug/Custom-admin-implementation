from django.contrib import admin
from .models import Client,Tags,ContactUser,ContactList,ClientPhoneNumber,BroadCast,Coupon,\
    ContactUserCoupon,Keyword,Days,Campaign,CampaignAction,ContactToCampaign,CustomFields,CustomFieldsValue,OneToOneMessage,ReferralCampaigns,ReferralCampaignToContact,ReferralRewardCouponContactUser
# Register your models here.
admin.site.register(Client)
admin.site.register(Tags)
admin.site.register(ContactList)
admin.site.register(ClientPhoneNumber)
admin.site.register(BroadCast)
admin.site.register(Coupon)
admin.site.register(ContactUserCoupon)
admin.site.register(ContactUser)
admin.site.register(Keyword)
admin.site.register(Days)
admin.site.register(Campaign)
admin.site.register(CampaignAction)
admin.site.register(ContactToCampaign)
admin.site.register(CustomFields)
admin.site.register(CustomFieldsValue)
admin.site.register(OneToOneMessage)
admin.site.register(ReferralCampaigns)
admin.site.register(ReferralCampaignToContact)
admin.site.register(ReferralRewardCouponContactUser)
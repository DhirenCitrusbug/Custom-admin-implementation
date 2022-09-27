from rest_framework import serializers
from .models import ContactUser, ContactList, ContactUserCoupon, Coupon, Tags, CustomFieldsValue, ReferralCampaigns, ReferralCampaignToContact ,Client,ReferralRewardCouponContactUser
from admin_user.models import Address,Country
from phonenumber_field.serializerfields import PhoneNumberField


class CountrySerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Country
        fields="__all__"


class AddressSerializer(serializers.ModelSerializer):
    country=CountrySerializer()
    
    class Meta:
        model=Address
        fields="__all__"

class ClientSerializer(serializers.ModelSerializer):
    address=AddressSerializer()

    class Meta:
        model=Client
        fields="__all__"


class ContactUserSerializer(serializers.ModelSerializer):
    phone_no1=serializers.SerializerMethodField()
    phone_no2=serializers.SerializerMethodField()
    tags_string=serializers.SerializerMethodField()
    active_campaign_string=serializers.SerializerMethodField()
    birth=serializers.SerializerMethodField()
    anniversary_date=serializers.SerializerMethodField()
    birth_month = serializers.SerializerMethodField()
    birth_date = serializers.SerializerMethodField()
    client=ClientSerializer()

    class Meta:
        model = ContactUser
        fields = "__all__"


    def get_phone_no1(self,obj):
        return f"+{obj.phone_no.country_code}"

    def get_phone_no2(self,obj):
        str1=str(obj.phone_no)
        country_code=f"+{obj.phone_no.country_code}"
        phone=str1.replace(country_code,'')
        return phone

    def get_tags_string(self,obj):
        a=""
        if obj.tags:
            for i in obj.tags.all():
                a=a+f"{i.id},"
            print(a)
            return a
        return ""

    def get_active_campaign_string(self,obj):
        a=""
        if obj.active_campaign:
            for i in obj.active_campaign.all():
                a=a+f"{i.id},"
            print(a)
            return a
        return ""

    def get_birth(self,obj):
        if obj.birthday:
            return obj.birthday.strftime("%m-%d")
        return ""

    def get_birth_month(self, obj):
        if obj.birthday:
            return int(obj.birthday.strftime("%m"))
        return ""

    def get_birth_date(self, obj):
        if obj.birthday:
            return int(obj.birthday.strftime("%d"))
        return ""

    def get_anniversary_date(self,obj):
        if obj.anniversary:
            return obj.anniversary.strftime("%m-%d")
        return ""


class ContactListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactList
        fields = "__all__"


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"

class ContactUserCouponSerializer(serializers.ModelSerializer):
    user=ContactUserSerializer()
    user_coupon=CouponSerializer()
    discount=serializers.SerializerMethodField()

    class Meta:
        model = ContactUserCoupon
        fields = "__all__"

    def get_discount(self,obj):
        if obj.amount:
            if obj.user_coupon.discount_type.lower()=="rs":
                return obj.user_coupon.discount_value
            else:
                return (obj.amount*obj.user_coupon.discount_value)/100
        return ""

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tags
        fields = "__all__"

class CustomFielsValueSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomFieldsValue
        fields = "__all__"


class ReferralCampaignSerializer(serializers.ModelSerializer):
    ref_coupon=CouponSerializer()
    reward_coupon=CouponSerializer()
    class Meta:
        model= ReferralCampaigns
        fields = "__all__"


class ContactUserReferralCampaignSerializer(serializers.ModelSerializer):
    contact_user=ContactUserSerializer()
    referral_camp=ReferralCampaignSerializer()

    class Meta:
        model = ReferralCampaignToContact
        fields = "__all__"

class ReferralRewardCouponContactUserSerializer(serializers.ModelSerializer):
    user=ContactUserSerializer()
    user_coupon=CouponSerializer()
    discount=serializers.SerializerMethodField()

    class Meta:
        model = ReferralRewardCouponContactUser
        fields = "__all__"

    def get_discount(self,obj):
        if obj.amount:
            if obj.user_coupon.discount_type.lower()=="rs":
                return obj.user_coupon.discount_value
            else:
                return (obj.amount*obj.user_coupon.discount_value)/100
        return ""
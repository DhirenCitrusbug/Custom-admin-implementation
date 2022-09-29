from django import forms
from django.core.exceptions import ValidationError

from .models import AgencyUser,Address, AgencyHostname
from admin_user.models import Country,State,TimeZone
import re
from admin_user.custom_hostname import create_custom_hostname, delete_custom_hostname


class AegencyChangeForm(forms.ModelForm):

    class Meta:
        model = AgencyUser
        fields = ["business_name","business_email",'business_phone_no','whitelabeldomian','time_zone','support_email']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['business_name'].widget.attrs.update({"placeholder": "Business Name"})
        self.fields['business_email'].widget.attrs.update({"placeholder": "Enter e-mail",})
        self.fields['business_phone_no'].widget.attrs.update({"placeholder": "Business Phone","maxlength":"10"})
        self.fields['time_zone'].queryset=TimeZone.objects.all().order_by('name')
        self.fields['time_zone'].empty_label = 'Select Time Zone'
        self.fields['time_zone'].widget.attrs.update({"class": "rw_cstm_dropdown"})

    def clean(self):
        cleaned_data = super(AegencyChangeForm, self).clean()
        business_name = cleaned_data.get('business_name')      

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


class AddressChangeForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ["address","state",'country','city','zip_code']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({"placeholder": "Enter Address"})
        self.fields['city'].widget.attrs.update({"placeholder": "City"})
        self.fields['zip_code'].widget.attrs.update({"placeholder": "Zip"})
        self.fields['country'].queryset=Country.objects.all().order_by('name')
        self.fields['country'].empty_label='Select Country'
        self.fields['country'].widget.attrs.update({"class": "rw_cstm_dropdown"})
        self.fields['state'].queryset=State.objects.all()
        self.fields['state'].empty_label='Select State/Region'
        self.fields['state'].widget.attrs.update({"class": "rw_cstm_dropdown"})

    def clean(self):
        cleaned_data = super(AddressChangeForm, self).clean()
        address = cleaned_data.get('address')

        #
        # if not address:
        #     raise ValidationError("Please add address")

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


class AegencyChangePasswordForm(forms.ModelForm):
    oldpassword = forms.CharField(max_length=250, widget=forms.PasswordInput, required=False)
    newpassword = forms.CharField(max_length=250, widget=forms.PasswordInput, required=False)
    confirmpassword = forms.CharField(max_length=250, widget=forms.PasswordInput, required=False)

    class Meta:
        model = AgencyUser
        fields = ['oldpassword','newpassword','confirmpassword']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['oldpassword'].widget.attrs.update(
            {"placeholder": "Current Password", "onselectstart": "return false" })
        self.fields['newpassword'].widget.attrs.update(
            {"placeholder": "New Password", "onselectstart": "return false"} )
        self.fields['confirmpassword'].widget.attrs.update(
            {"placeholder": "Confirm Password", "onselectstart": "return false"})

    def clean(self):
        cleaned_data = super(AegencyChangePasswordForm, self).clean()
        oldpassword = cleaned_data.get('oldpassword')
        confirmpassword = cleaned_data.get('confirmpassword')
        newpassword = cleaned_data.get('newpassword')

        if oldpassword:
            user = self.instance
            if not user.check_password(oldpassword):
                raise forms.ValidationError("Please enter correct Old Password")
            else:
                if not newpassword:
                    raise forms.ValidationError(
                        "Please enter Password"
                    )
                if not re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*])[\w\d!@#$%^&*]{6,20}$",newpassword):
                    raise forms.ValidationError(
                        "Password should be of at least 6 char with 1 capital,1 small, 1 special char in it."
                    )
                if not confirmpassword:
                    raise forms.ValidationError(
                        "Please enter Confirm Password"
                    )
                if not confirmpassword == newpassword:
                    raise forms.ValidationError("Password and Confirm Password does not match")
                if confirmpassword == newpassword:
                    user.set_password(confirmpassword)
        if newpassword or oldpassword:
            if not oldpassword:
                raise ValidationError("Please enter Current Password")

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


class AegencyWhitelabelDomainForm(forms.ModelForm):
    
    class Meta:
        model = AgencyUser
        fields = ['whitelabeldomian', 'support_email','host']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['whitelabeldomian'].widget.attrs.update({"placeholder": "Whitelabel Domain"})
        self.fields['support_email'].widget.attrs.update({"placeholder": "Enter Support Email Address",})

    def clean(self):
        cleaned_data = super(AegencyWhitelabelDomainForm, self).clean()
        whitelabeldomian = cleaned_data.get('whitelabeldomian')
        cleaned_data['host'] = self.instance.host
        if self.instance.whitelabeldomian:
            if whitelabeldomian:
                if not self.instance.whitelabeldomian == whitelabeldomian:
                    response = create_custom_hostname(whitelabeldomian)
                    if str(response['success']) == 'True':
                        host_obj=AgencyHostname.objects.create(user=self.instance, host_id=response['result']['id'],
                                                      hostname=response['result']['hostname'], response=response)
                        agency_user=AgencyUser.objects.filter(id=self.instance.id).first()
                        print(agency_user,"sdasdasd")
                        if agency_user:
                            agency_user.host=host_obj
                            agency_user.save()
                        delete_custom_hostname(self.instance.host.host_id)
                        cleaned_data['host'] = host_obj
                    else:
                        print(response)
                        print(response['errors'])
                        if (response['errors'][0])['code'] == 1406 :
                            raise forms.ValidationError("This whitelabel domain already exists")
                        raise forms.ValidationError((response['errors'][0])['message'])
            else:
                delete_custom_hostname(self.instance.host.host_id)
        else:
            if whitelabeldomian:
                if not self.instance.whitelabeldomian == whitelabeldomian:
                    response = create_custom_hostname(whitelabeldomian)
                    if str(response['success']) == 'True':
                        host_obj=AgencyHostname.objects.create(user=self.instance, host_id=response['result']['id'],
                                                      hostname=response['result']['hostname'], response=response)
                        cleaned_data['host'] = host_obj
                    else:
                        if (response['errors'][0])['code'] == 1406 :
                            raise forms.ValidationError("This whitelabel domain already exists")
                        raise forms.ValidationError((response['errors'][0])['message'])

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
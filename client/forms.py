from django import forms
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
import re
from .models import Client,ContactUser
from admin_user.models import Address, Admin, TimeZone

class ClientEditProfileForm(forms.ModelForm):
    oldpassword = forms.CharField(max_length=250, widget=forms.PasswordInput, required=False)
    newpassword = forms.CharField(max_length=250, widget=forms.PasswordInput, required=False)
    confirmpassword = forms.CharField(max_length=250, widget=forms.PasswordInput, required=False)

    class Meta:
        model = Client
        fields = [ "oldpassword", "first_name", "last_name", "newpassword", "confirmpassword"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['oldpassword'].widget.attrs.update(
            {"placeholder": "Current Password", "onselectstart": "return false"})
        self.fields['newpassword'].widget.attrs.update(
            {"placeholder": "New password", "onselectstart": "return false"})
        self.fields['confirmpassword'].widget.attrs.update(
            {"placeholder": "Confirm password", "onselectstart": "return false"})
        self.fields['first_name'].widget.attrs.update(
            {"placeholder": "First Name"})
        self.fields['last_name'].widget.attrs.update(
            {"placeholder": "Last Name"})

    def clean(self):
        cleaned_data = super(ClientEditProfileForm, self).clean()
        oldpassword = cleaned_data.get('oldpassword')
        confirmpassword = cleaned_data.get('confirmpassword')
        newpassword = cleaned_data.get('newpassword')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if oldpassword:
            user = self.instance
            if not user.check_password(oldpassword):
                raise forms.ValidationError("Please enter correct Old Password")
            else:
                if not newpassword:
                    raise forms.ValidationError(
                        "Please enter Password"
                    )
                if not re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*])[\w\d!@#$%^&*]{6,20}$", newpassword):
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
        if not first_name:
            raise ValidationError("Please add First name")
        if not last_name:
            raise ValidationError("Please add Last name")


    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance


class ClientChangeForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ["business_name","business_email",'business_phone_no','time_zone','email']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['business_name'].widget.attrs.update({"placeholder": "Business Name"})
        self.fields['business_email'].widget.attrs.update({"placeholder": "Business Email",})
        self.fields['email'].widget.attrs.update({"placeholder": "Enter e-mail"})
        self.fields['business_phone_no'].widget.attrs.update({"placeholder": "Business Phone"})
        self.fields['time_zone'].queryset=TimeZone.objects.all().order_by('name')
        self.fields['time_zone'].empty_label = 'Select Time Zone'
        self.fields['time_zone'].widget.attrs.update({"class": "rw_cstm_dropdown"})

    def clean(self):
        cleaned_data = super(ClientChangeForm, self).clean()
        print(cleaned_data,'cleaned_data')
        business_name = cleaned_data.get('business_name')
        email = cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Please add Email")

        if Admin.objects.filter(email=email).exclude(id=self.instance.id):
            raise forms.ValidationError("Email already exists")

    # def clean_email(self):
    #     data = self.cleaned_data['email']
    #     if not data:
    #         raise forms.ValidationError("please enter email")
    #     else:
    #         return data



    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


class ContactCreateForm(forms.ModelForm):
    phone_no=PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='IN',attrs={'class':'form-control'}))
    class Meta:
        model = ContactUser
        fields = ["phone_no","first_name",'last_name','birthday','anniversary','tags','time_zone']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['phone_no'].widget.attrs.update({"placeholder": "Phone Number","type":"number"})
        self.fields['phone_no'].required=False
        self.fields['first_name'].widget.attrs.update({"placeholder": "First Name"})
        self.fields['last_name'].widget.attrs.update({"placeholder": "Last Name"})
        self.fields['birthday'].widget.attrs.update({"placeholder": "MM-DD","class":"date_input","readonly":'true'})
        self.fields['anniversary'].widget.attrs.update({"placeholder": "MM-DD","class":"date_input","readonly":'true'})
        self.fields['time_zone'].queryset=TimeZone.objects.all().order_by('name')
        self.fields['time_zone'].empty_label = 'Select Time Zone'
        self.fields['time_zone'].widget.attrs.update({"class": "rw_popup_cstm_dropdown","id":"c_time_zone"})
        # self.fields['tags'].widget.attrs.update({"class": "js-states form-control", "multiple":"multiple"})

    def clean(self):
        cleaned_data = super(ContactCreateForm, self).clean()



    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


class ContactChangeForm(forms.ModelForm):
    phone_no=PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='IN',attrs={'class':'form-control'}))
    class Meta:
        model = ContactUser
        fields = ["phone_no","first_name",'last_name','birthday','anniversary','tags','time_zone','active_campaign']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['phone_no'].widget.attrs.update({"placeholder": "Phone Number","id":"phone","type":"number"})
        self.fields['phone_no'].required=False
        self.fields['first_name'].widget.attrs.update({"placeholder": "First Name","id":"f_name"})
        self.fields['last_name'].widget.attrs.update({"placeholder": "Last Name","id":"l_name"})
        self.fields['birthday'].widget.attrs.update({"placeholder": "MM-DD","id":"birth","class":"date_input","readonly":'true'})
        self.fields['anniversary'].widget.attrs.update({"placeholder": "MM-DD","id":"annivarsary_edit","class":"date_input","readonly":'true'})
        self.fields['time_zone'].queryset=TimeZone.objects.all().order_by('name')
        self.fields['time_zone'].empty_label = 'Select Time Zone'
        self.fields['time_zone'].widget.attrs.update({"class": "rw_popup_cstm_dropdown","id":"e_time_zone"})
        # self.fields['tags'].widget.attrs.update({"class": "js-states form-control", "multiple":"multiple","id":"edit_cont"})
        self.fields['active_campaign'].widget.attrs.update({"class": "js-states form-control", "multiple":"multiple","id":"active_campaigns1"})

    def clean(self):
        cleaned_data = super(ContactChangeForm, self).clean()



    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

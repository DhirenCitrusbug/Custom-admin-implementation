from django import forms
from django.core.exceptions import ValidationError

from .models import Admin
from aegency_user.models import AgencyUser
import re

class EditProfileForm(forms.ModelForm):
    oldpassword = forms.CharField(max_length=250, widget=forms.PasswordInput, required=False)
    newpassword = forms.CharField(max_length=250, widget=forms.PasswordInput, required=False)
    confirmpassword = forms.CharField(max_length=250, widget=forms.PasswordInput, required=False)

    class Meta:
        model = Admin
        fields = [ "oldpassword", "first_name", "last_name", "newpassword", "confirmpassword",'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['oldpassword'].widget.attrs.update(
            {"placeholder": "Current Password", "onselectstart": "return false" })
        self.fields['newpassword'].widget.attrs.update(
            {"placeholder": "New Password", "onselectstart": "return false"} )
        self.fields['confirmpassword'].widget.attrs.update(
            {"placeholder": "Confirm Password", "onselectstart": "return false"})
        self.fields['first_name'].widget.attrs.update(
            {"placeholder": "First Name"})
        self.fields['last_name'].widget.attrs.update(
            {"placeholder": "Last Name"})

    def clean(self):
        cleaned_data = super(EditProfileForm, self).clean()
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
        if not first_name:
            raise ValidationError("Please add First name")
        if not last_name:
            raise ValidationError("Please add Last name")


    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance


class AegencyCreationForm(forms.ModelForm):

    class Meta:
        model = AgencyUser
        fields = ["email", "password", "first_name", "last_name", "business_name", "plan_duration",'transaction_id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        plans=[('0','Plan Duration'),('1','1 Month'),('2','6 Months'),('3','12 Months'),('4','24 Months'),('5','Lifetime')]
        self.fields['email'].widget.attrs.update({"placeholder": "Email"})
        self.fields['business_name'].widget.attrs.update({"placeholder": "Business Name",})
        self.fields['password'].widget.attrs.update({"placeholder": "Password",})
        self.fields['transaction_id'].widget.attrs.update({"placeholder": "Enter ID"})
        self.fields['first_name'].widget.attrs.update({"placeholder": "First Name"})
        self.fields['last_name'].widget.attrs.update({"placeholder": "Last Name"})
        self.fields['plan_duration']=forms.ChoiceField(choices=plans)
        self.fields['plan_duration'].widget.attrs.update({"class": "rw_popup_cstm_dropdown"})
    def clean(self):
        cleaned_data = super(AegencyCreationForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        business_name = cleaned_data.get('business_name')

        if not first_name:
            raise ValidationError("Please add First name")
        if not last_name:
            raise ValidationError("Please add Last name")
        if not email:
            raise ValidationError("Please add Email")
        if not password:
            raise ValidationError("Please add password")
        if not business_name:
            raise ValidationError("Please add business name")

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance

class AgencyEditForm(forms.ModelForm):

    class Meta:
        model = AgencyUser
        fields = ["email", "first_name", "last_name", "business_name", 'business_phone_no']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({"placeholder": "Enter e-mail"})
        self.fields['business_name'].widget.attrs.update({"placeholder": "Business Name"})
        self.fields['first_name'].widget.attrs.update({"placeholder": "First Name"})
        self.fields['last_name'].widget.attrs.update({"placeholder": "Last Name"})
        self.fields['business_phone_no'].widget.attrs.update({"placeholder": "Bussiness Phone No"})


    def clean(self):
        cleaned_data = super(AgencyEditForm, self).clean()
        email = cleaned_data.get('email')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        business_name = cleaned_data.get('business_name')

        if not first_name:
            raise ValidationError("Please add First name")
        if not last_name:
            raise ValidationError("Please add Last name")
        if not email:
            raise ValidationError("Please add Email")
        if not business_name:
            raise ValidationError("Please add business name")

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance
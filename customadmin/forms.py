from dataclasses import field
from pyexpat import model
from django import forms
from aegency_user.models import AgencyUser
from client.models import Client
from client.forms import ClientChangeForm
from aegency_user.forms import AegencyChangeForm
import re

from customadmin.views import agency

class AgencyCreateForm(forms.ModelForm):
    class Meta:
        model = AgencyUser
        fields = ['first_name','last_name','email','business_name','transaction_id','plan_duration','owner']
    def __init__(self, *args, **kwargs):
        super(AgencyCreateForm,self).__init__(*args, **kwargs)
        self.fields['owner'].required = False
    def clean(self):
            try:
                owner = self.cleaned_data['owner']
                if not owner:
                    self.fields['owner'].widget.attrs['style'] = 'border:1px solid red'
                    raise forms.ValidationError("Owner Field is Required")
            except:
                raise forms.ValidationError("Owner Field is Required")
            first_name = self.cleaned_data['first_name']
            if not first_name:
                self.fields['first_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("First Name is Required")
            if not re.match(r'^[A-Za-z]+$', str(first_name)):
                self.fields['first_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Enter Valid First Name")
            last_name = self.cleaned_data['last_name']
            if not last_name:
                raise forms.ValidationError("Last Name is Required")
            if not re.match(r'^[A-Za-z]+$', str(last_name)):
                raise forms.ValidationError("Enter Valid Last Name")
            business_name = self.cleaned_data['business_name']
            print(business_name)
            if not first_name:
                raise forms.ValidationError("Business Name is Required")
            if not re.match(r'^[A-Za-z]+$',  str(business_name)):
                raise forms.ValidationError("Enter Valid Business Name")
            email = self.cleaned_data['email']
            if not email:
                raise forms.ValidationError("This Field is Required")
            if not re.match(r'^[A-Za-z0-9._@]+$', str(email)):
                raise forms.ValidationError("Enter Valid Email")



    # def clean_first_name(self):
    #         first_name = self.cleaned_data['first_name']
    #         if not first_name:
    #             raise forms.ValidationError("This Field is Required")
    #         if not re.match(r'^[A-Za-z]+$', str(first_name)):
    #             raise forms.ValidationError("Enter Valid First Name")
    #         return first_name

    # def clean_last_name(self):
    #         last_name = self.cleaned_data['last_name']
    #         if not last_name:
    #             raise forms.ValidationError("This Field is Required")
    #         if not re.match(r'^[A-Za-z]+$', str(last_name)):
    #             raise forms.ValidationError("Enter Valid Last Name")
    #         return last_name
              
    # def clean_business_name(self):
    #         business_name = self.cleaned_data['business_name']
    #         print(business_name)
    #         if not re.match(r'^[A-Za-z]+$',  str(business_name)):
    #             raise forms.ValidationError("Enter Valid Business Name")
    #         return business_name

    # def clean_email(self):
    #         email = self.cleaned_data['email']
    #         if not email:
    #             raise forms.ValidationError("This Field is Required")
    #         if not re.match(r'^[A-Za-z]+$', str(email)):
    #             raise forms.ValidationError("Enter Valid Last Name")
    #         return email

class ClientCreateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name','last_name','business_name','business_email','business_phone_no','aegency','email']


         
    def clean(self):
            try:
                agency = self.cleaned_data['agency']
                if not agency:
                    raise forms.ValidationError("Agency Field is Required")
            except:
                pass
            first_name = self.cleaned_data['first_name']
            if not first_name:
                raise forms.ValidationError("First Name is Required")
            if not re.match(r'^[A-Za-z]+$', str(first_name)):
                raise forms.ValidationError("Enter Valid First Name")

            last_name = self.cleaned_data['last_name']
            if not last_name:
                raise forms.ValidationError("Last Name is Required")
            if not re.match(r'^[A-Za-z]+$', str(last_name)):
                raise forms.ValidationError("Enter Valid Last Name")

            business_name = self.cleaned_data['business_name']
            if not first_name:
                raise forms.ValidationError("This Field is Required")
            if not re.match(r'^[A-Za-z]+$',  str(business_name)):
                raise forms.ValidationError("Enter Valid Business Name")

            business_email = self.cleaned_data['business_email']
            if not business_name:
                raise forms.ValidationError("This Field is Required")
            if not re.match(r'^[A-Za-z0-9._@]+$',  str(business_email)):
                raise forms.ValidationError("Enter Valid Business Email")

            business_phone_no = self.cleaned_data['business_phone_no']
            if not business_phone_no:
                raise forms.ValidationError("This Field is Required")
            if not re.match(r'^[0-9]+$',  str(business_phone_no)):
                raise forms.ValidationError("Enter Valid Phone No.")

            email = self.cleaned_data['email']
            if not email:
                raise forms.ValidationError("This Field is Required")
            if not re.match(r'^[A-Za-z0-9._@]+$', str(email)):
                raise forms.ValidationError("Enter Valid Email")



class MyClientChangeForm(ClientChangeForm):
    
    class Meta:
        model = Client
        fields = ['first_name','last_name','business_name','business_email','business_phone_no','time_zone','email']

    def __init__(self, *args, **kwargs):
        super(MyClientChangeForm).__init__(*args, **kwargs)
        self.fields['owner'].widget.attrs.required = False
    def clean(self):
            try:
                agency = self.cleaned_data['agency']
                if not agency:
                    raise forms.ValidationError("Agency Field is Required")
            except:
                pass
            first_name = self.cleaned_data['first_name']
            if not first_name:
                
                raise forms.ValidationError("First Name is Required")
            if not re.match(r'^[A-Za-z]+$', str(first_name)):
                raise forms.ValidationError("Enter Valid First Name")

            last_name = self.cleaned_data['last_name']
            if not last_name:
                raise forms.ValidationError("Last Name is Required")
            if not re.match(r'^[A-Za-z]+$', str(last_name)):
                raise forms.ValidationError("Enter Valid Last Name")

            business_name = self.cleaned_data['business_name']
            if not first_name:
                raise forms.ValidationError("This Field is Required")
            if not re.match(r'^[A-Za-z]+$',  str(business_name)):
                raise forms.ValidationError("Enter Valid Business Name")

            business_email = self.cleaned_data['business_email']
            if not business_name:
                raise forms.ValidationError("This Field is Required")
            if not re.match(r'^[A-Za-z0-9._@]+$',  str(business_email)):
                raise forms.ValidationError("Enter Valid Business Email")

            business_phone_no = self.cleaned_data['business_phone_no']
            if not business_phone_no:
                raise forms.ValidationError("This Field is Required")
            if not re.match(r'^[0-9]+$',  str(business_phone_no)):
                raise forms.ValidationError("Enter Valid Phone No.")

            email = self.cleaned_data['email']
            if not email:
                raise forms.ValidationError("This Field is Required")
            if not re.match(r'^[A-Za-z0-9._@]+$', str(email)):
                raise forms.ValidationError("Enter Valid Email")
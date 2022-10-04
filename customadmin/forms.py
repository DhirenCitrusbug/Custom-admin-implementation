from dataclasses import field
from pyexpat import model
from django import forms
from aegency_user.models import AgencyUser
from client.models import Client
from client.forms import ClientChangeForm
from aegency_user.forms import AegencyChangeForm
import re
import random
import string
from customadmin.views import agency

class AgencyCreateForm(forms.ModelForm):
    class Meta:
        model = AgencyUser
        fields = ['first_name','last_name','email','business_name','transaction_id','plan_duration','owner','password']
    def __init__(self, *args, **kwargs):
        super(AgencyCreateForm,self).__init__(*args, **kwargs)
        self.fields['owner'].required = False
        self.fields['password'].widget = forms.HiddenInput()
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
                self.fields['last_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Last Name is Required")
            if not re.match(r'^[A-Za-z]+$', str(last_name)):
                self.fields['last_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Enter Valid Last Name")
            business_name = self.cleaned_data['business_name']
            print(business_name)
            if not business_name:
                self.fields['business_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Business Name is Required")
            if not re.match(r'^[A-Za-z]+$',  str(business_name)):
                self.fields['business_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Enter Valid Business Name")
            email = self.cleaned_data['email']
            if not email:
                
                self.fields['email'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("This Field is Required")
            if not re.match(r'^[A-Za-z0-9._@]+$', str(email)):
                self.fields['email'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Enter Valid Email")
            password = self.cleaned_data['password']
            if not password:
                password = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=10))
                self.cleaned_data['password'] = password
                print(self.cleaned_data)

    # def save(self, *args, **kwargs):
    #     password = ''.join(random.choices(
    #     string.ascii_uppercase + string.digits, k=10))
    #     self.cleaned_data['password'] = password
    #     print(self.fields,self)
    #     super().save(*args, *kwargs)

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
        fields = ['first_name','last_name','business_name','business_email','business_phone_no','aegency','email','password']
    def __init__(self, *args, **kwargs):
        super(ClientCreateForm,self).__init__(*args, **kwargs)
        self.fields['aegency'].required = False
        self.fields['password'].widget = forms.HiddenInput()

         
    def clean(self):
            agency = self.cleaned_data['aegency']
            if not agency:
                self.fields['aegency'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Agency Field is Required")

            first_name = self.cleaned_data['first_name']
            if not first_name:
                self.fields['first_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("First Name is Required")
            if not re.match(r'^[A-Za-z]+$', str(first_name)):
                self.fields['first_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Enter Valid First Name")

            last_name = self.cleaned_data['last_name']
            if not last_name:
                self.fields['last_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Last Name is Required")
            if not re.match(r'^[A-Za-z]+$', str(last_name)):
                self.fields['last_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Enter Valid Last Name")

            business_name = self.cleaned_data['business_name']
            if not first_name:
                self.fields['business_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("This Field is Required")
            if not re.match(r'^[A-Za-z]+$',  str(business_name)):
                self.fields['business_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Enter Valid Business Name")

            business_email = self.cleaned_data['business_email']
            if not business_name:
                self.fields['business_email'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("This Field is Required")
            if not re.match(r'^[A-Za-z0-9._@]+$',  str(business_email)):
                self.fields['business_email'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Enter Valid Business Email")

            business_phone_no = self.cleaned_data['business_phone_no']
            if not business_phone_no:
                self.fields['business_phone_no'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("This Field is Required")
            if not re.match(r'^[0-9]+$',  str(business_phone_no)):
                self.fields['business_phone_no'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Enter Valid Phone No.")

            email = self.cleaned_data['email']
            if not email:
                self.fields['email'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("This Field is Required")
            if not re.match(r'^[A-Za-z0-9._@]+$', str(email)):
                self.fields['email'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Enter Valid Email")

            password = self.cleaned_data['password']
            if not password:
                password = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=10))
                self.cleaned_data['password'] = password
                print(self.cleaned_data)
            



class MyClientChangeForm(ClientChangeForm):
    
    class Meta:
        model = Client
        fields = ['first_name','last_name','business_name','business_email','business_phone_no','time_zone','email']


    def clean(self):
            try:
                agency = self.cleaned_data['aegency']
                if not agency:
                    self.fields['aegency'].widget.attrs['style'] = 'border:1px solid red'
                    raise forms.ValidationError("Agency Field is Required")
            except:
                pass
            first_name = self.cleaned_data['first_name']
            if not first_name:
                self.fields['first_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("First Name is Required")
            if not re.match(r'^[A-Za-z]+$', str(first_name)):
                self.fields['first_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Enter Valid First Name")

            last_name = self.cleaned_data['last_name']
            if not last_name:
                self.fields['last_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Last Name is Required")
            if not re.match(r'^[A-Za-z]+$', str(last_name)):
                self.fields['last_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Enter Valid Last Name")

            business_name = self.cleaned_data['business_name']
            if not business_name:
                self.fields['business_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("This Field is Required")
            if not re.match(r'^[A-Za-z]+$',  str(business_name)):
                self.fields['business_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Enter Valid Business Name")

            business_email = self.cleaned_data['business_email']
            if not business_email:
                self.fields['business_email'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("This Field is Required")
            if not re.match(r'^[A-Za-z0-9._@]+$',  str(business_email)):
                self.fields['business_email'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Enter Valid Business Email")

            business_phone_no = self.cleaned_data['business_phone_no']
            if not business_phone_no:
                self.fields['business_phone_no'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("This Field is Required")
            if not re.match(r'^[0-9]+$',  str(business_phone_no)):
                self.fields['business_phone_no'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Enter Valid Phone No.")

            email = self.cleaned_data['email']
            if not email:
                self.fields['email'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("This Field is Required")
            if not re.match(r'^[A-Za-z0-9._@]+$', str(email)):
                self.fields['email'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Enter Valid Email")




class MyAegencyChangeForm(AegencyChangeForm):

    class Meta:
        model = AgencyUser
        fields = ["first_name","last_name","business_name","business_email",'business_phone_no','whitelabeldomian','time_zone','support_email']




    def clean(self):
            first_name = self.cleaned_data['first_name']
            if not first_name:
                self.fields['first_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("First Name is Required")
            if not re.match(r'^[A-Za-z]+$', str(first_name)):
                self.fields['first_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Enter Valid First Name")

            last_name = self.cleaned_data['last_name']
            if not last_name:
                self.fields['last_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Last Name is Required")
            if not re.match(r'^[A-Za-z]+$', str(last_name)):
                self.fields['last_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Enter Valid Last Name")
            business_name = self.cleaned_data['business_name']
            if not business_name:
                self.fields['business_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("This Field is Required")
            if not re.match(r'^[A-Za-z]+$',  str(business_name)):
                self.fields['business_name'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Enter Valid Business Name")

            business_email = self.cleaned_data['business_email']
            if not business_email:
                self.fields['business_email'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("This Field is Required")
            if not re.match(r'^[A-Za-z0-9._@]+$',  str(business_email)):
                self.fields['business_email'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Enter Valid Business Email")

            business_phone_no = self.cleaned_data['business_phone_no']
            if not business_phone_no:
                self.fields['business_phone_no'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("This Field is Required")
            if not re.match(r'^[0-9]+$',  str(business_phone_no)):
                self.fields['business_phone_no'].widget.attrs['style'] = 'border:1px solid red'
                raise forms.ValidationError("Enter Valid Phone No.")
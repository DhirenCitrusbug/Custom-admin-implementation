from dataclasses import field
from pyexpat import model
from django import forms
from aegency_user.models import AgencyUser
from client.models import Client



class AgencyCreateForm(forms.ModelForm):
    class Meta:
        model = AgencyUser
        fields = ['first_name','last_name','email','business_name','transaction_id','plan_duration','owner']

class ClientCreateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name','last_name','business_name','business_email','business_phone_no','aegency','email']

class ClientChangeForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ['first_name','last_name','business_name','business_email','business_phone_no','time_zone','email']
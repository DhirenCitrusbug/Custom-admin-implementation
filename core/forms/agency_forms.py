from django import forms

from core.models.agency import AgencyUser, TimeZone


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
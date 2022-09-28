from django import forms
from core.models import TrustedAccessories
from django.forms.widgets import TextInput
import validators


# -----------------------------------------------------------------------------
# TrustedAccessories
# -----------------------------------------------------------------------------
class TrustedAccessoriesCreationForm(forms.ModelForm):
    """Custom TrustedAccessories"""
    featured_image = forms.ImageField(required=True)

    class Meta:
        model = TrustedAccessories
        exclude = ('create_by', 'create_at', 'update_at')
        labels = {
            'slide_link': 'Ad link URL',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['featured_image']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'autofocus': 'autofocus'})

    def clean(self):
        cleaned_data = super(TrustedAccessoriesCreationForm, self).clean()
        name = cleaned_data.get("name")
        slide_link = cleaned_data.get("slide_link")
        featured_image = cleaned_data.get("featured_image")

        if not name:
            raise forms.ValidationError("Please enter name.")

        if slide_link:
            valid = validators.url(slide_link)
            if valid is not True:
                raise forms.ValidationError("Please enter valid link.")

        if featured_image:
            if featured_image.size > 15097152:
                raise forms.ValidationError("Please select image below 15 mb!")

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance


class TrustedAccessoriesChangeForm(forms.ModelForm):
    """Custom form to change TrustedAccessories"""
    featured_image = forms.ImageField(required=True)

    class Meta:
        model = TrustedAccessories
        exclude = ('create_by', 'create_at', 'update_at')
        labels = {
            'slide_link': 'Ad link URL',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['featured_image']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'autofocus': 'autofocus'})

    def clean(self):
        cleaned_data = super(TrustedAccessoriesChangeForm, self).clean()
        name = cleaned_data.get("name")
        slide_link = cleaned_data.get("slide_link")
        featured_image = cleaned_data.get("featured_image")
        if not name:
            raise forms.ValidationError("Please enter name.")

        if slide_link:
            valid = validators.url(slide_link)
            if valid is not True:
                raise forms.ValidationError("Please enter valid link.")

        if featured_image:
            if featured_image.size > 15097152:
                raise forms.ValidationError("Please select image below 15 mb!")

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance


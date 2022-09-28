# -*- coding: utf-8 -*-

from django import forms
# from core.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm


# -----------------------------------------------------------------------------
# User
# -----------------------------------------------------------------------------
class UserChangeForm(UserChangeForm):
    """Custom form to change User"""
    profile_image = forms.ImageField(widget=forms.FileInput, required=False)

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = [
            "email",
            "full_name",
            "profile_image",
            # "is_staff",
            # "is_superuser"
        ]
        labels = {
            "profile_image": "Profile Image (Size:180px x 180px)",
            # "is_staff": "Staff Member",
            # "is_superuser": "Super Admin",
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'attrs': 'readonly'})
        self.fields['full_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['profile_image'].widget.attrs.update({'class': 'form-control'})
        # self.fields['is_staff'].widget.attrs.update({'class': 'form-control'})
        # self.fields['is_staff'].widget.attrs['disabled'] = True
        # self.fields['is_superuser'].widget.attrs.update({'class': 'form-control'})
        # self.fields['is_superuser'].widget.attrs['disabled'] = True
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super(UserChangeForm, self).clean()
        email = cleaned_data.get("email").strip().lower()
        full_name = cleaned_data.get("full_name")
        if not email:
            raise forms.ValidationError(
                "Please add email."
            )
        if not full_name:
            raise forms.ValidationError(
                "Please add name."
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.email = instance.email.strip().lower()
        if commit:
            instance.save()

        return instance


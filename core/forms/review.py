# -*- coding: utf-8 -*-
from django import forms
from core.models import Review, ReviewGalley
from datetime import datetime, date
from django.utils.translation import ugettext_lazy as _


# -----------------------------------------------------------------------------
# Review
# -----------------------------------------------------------------------------
class ReviewCreationForm(forms.ModelForm):
    """Custom Review"""
    slug = forms.CharField(required=False)
    publish_date = forms.DateField(
        required=True, input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
        initial=date.today(),
    )
    image_galley = forms.ImageField(required=False)

    class Meta:
        model = Review
        exclude = ('create_by', 'create_at', 'update_at')
        widgets = {
            'categories': forms.SelectMultiple(attrs={'value': '', 'id': 'categorieslist'}),
            'brands': forms.SelectMultiple(attrs={'value': '', 'id': 'brandslist'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'featured_image' and field != 'image_galley':
                self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super(ReviewCreationForm, self).clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")

        if not name:
            raise forms.ValidationError("Please enter Title.")

        if not description:
            raise forms.ValidationError("Please enter Description.")

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


class ReviewChangeForm(forms.ModelForm):
    """Custom form to change Review"""

    publish_date = forms.DateField(
        required=True, input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
    )
    update_at = forms.DateField(
        required=True, input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
    )

    class Meta:
        model = Review
        exclude = ('create_by', 'create_at')
        widgets = {
            'categories': forms.SelectMultiple(attrs={'value': '', 'id': 'categorieslist'}),
            'brands': forms.SelectMultiple(attrs={'value': '', 'id': 'brandslist'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'featured_image':
                self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['publish_date'].label = "Publish Date"

    def clean(self):
        cleaned_data = super(ReviewChangeForm, self).clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")

        if not name:
            raise forms.ValidationError("Please enter Title.")

        if not description:
            raise forms.ValidationError("Please enter Description.")

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

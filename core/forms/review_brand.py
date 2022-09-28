# -*- coding: utf-8 -*-
from django import forms
from core.models import ReviewBrand
from django.core.validators import FileExtensionValidator

# -----------------------------------------------------------------------------
# ReviewBrand
# -----------------------------------------------------------------------------
class ReviewBrandCreationForm(forms.ModelForm):
    """Custom ReviewBrand"""
    slug = forms.CharField(required=False)
    brand_image_full = forms.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=["png"])],
        label='Brand image color (1000x500px, .png with transparent background, brand-logo-c.png)'
    )
    brand_image_grayscale_full = forms.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=["png"])],
        label='Brand image grayscale (1000x500px, .png with transparent background, brand-logo-g.png)'
    )
    brand_image_darkmode_full = forms.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=["png"])],
        label='Brand image darkmode (1000x500px, .png with transparent background, brand-logo-w.png)'
    )
    meta_title = forms.CharField(required=True, label='Meta Title', widget=forms.TextInput(attrs={'placeholder': '| ElectricBikeReview.com', 'readonly': True}))

    class Meta:
        model = ReviewBrand
        fields = [
            'name', 'slug', 'meta_title', 'description', 'parent_brand', 'brand_image_full', 'status', 'featured_review',
            'brand_image_grayscale_full', 'brand_image_darkmode_full', 'short_description'
        ]
        labels = {
            "brand_image_full": "Brand image color (1000x500px, .png with transparent background, brand-logo-c.png)",
            "brand_image_grayscale_full": "Brand image grayscale (1000x500px, .png with transparent background, brand-logo-g.png)",
            "brand_image_darkmode_full": "Brand image darkmode (1000x500px, .png with transparent background, brand-logo-w.png)",
            "short_description": "Short Description(Meta Tags)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['brand_image_full', 'brand_image_grayscale_full', 'brand_image_darkmode_full']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields['name'].widget.attrs.update({'autofocus': 'autofocus'})

    def clean(self):
        cleaned_data = super(ReviewBrandCreationForm, self).clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")
        brand_image_full = cleaned_data.get("brand_image_full")
        brand_image_grayscale_full = cleaned_data.get("brand_image_grayscale_full")
        brand_image_darkmode_full = cleaned_data.get("brand_image_darkmode_full")

        if not name:
            raise forms.ValidationError("Please enter Title.")

        if not description:
            raise forms.ValidationError("Please enter Description.")

        if brand_image_full:
            if brand_image_full.size > 15097152:
                raise forms.ValidationError("Please select image below 15 mb!")

        if brand_image_grayscale_full:
            if brand_image_grayscale_full.size > 15097152:
                raise forms.ValidationError("Please select image below 15 mb!")

        if brand_image_darkmode_full:
            if brand_image_darkmode_full.size > 15097152:
                raise forms.ValidationError("Please select image below 15 mb!")

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


class ReviewBrandChangeForm(forms.ModelForm):
    """Custom form to change ReviewBrand"""
    meta_title = forms.CharField(required=True, label='Meta Title')
    brand_image_full = forms.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=["png"])],
        label='Brand image color (1000x500px, .png with transparent background, brand-logo-c.png)'
    )
    brand_image_grayscale_full = forms.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=["png"])],
        label='Brand image grayscale (1000x500px, .png with transparent background, brand-logo-g.png)'
    )
    brand_image_darkmode_full = forms.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=["png"])],
        label='Brand image darkmode (1000x500px, .png with transparent background, brand-logo-w.png)'
    )
    meta_title = forms.CharField(required=True, label='Meta Title', widget=forms.TextInput(attrs={'placeholder': '| ElectricBikeReview.com', 'readonly': True}))

    class Meta:
        model = ReviewBrand
        fields = [
            'name', 'slug', 'meta_title', 'description', 'parent_brand', 'brand_image_full', 'status', 'featured_review',
            'brand_image_grayscale_full', 'brand_image_darkmode_full', 'short_description'
        ]
        labels = {
            "brand_image_full": "Brand image color (1000x500px, .png with transparent background, brand-logo-c.png)",
            "brand_image_grayscale_full": "Brand image grayscale (1000x500px, .png with transparent background, brand-logo-g.png)",
            "brand_image_darkmode_full": "Brand image darkmode (1000x500px, .png with transparent background, brand-logo-w.png)",
            "short_description": "Short Description(Meta Tags)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['brand_image_full', 'brand_image_grayscale_full', 'brand_image_darkmode_full']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields['name'].widget.attrs.update({'autofocus': 'autofocus'})

    def clean(self):
        cleaned_data = super(ReviewBrandChangeForm, self).clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")
        brand_image_full = cleaned_data.get("brand_image_full")
        brand_image_grayscale_full = cleaned_data.get("brand_image_grayscale_full")
        brand_image_darkmode_full = cleaned_data.get("brand_image_darkmode_full")

        if not name:
            raise forms.ValidationError("Please enter Title.")

        if not description:
            raise forms.ValidationError("Please enter Description.")

        if brand_image_full:
            if brand_image_full.size > 15097152:
                raise forms.ValidationError("Please select image below 15 mb!")

        if brand_image_grayscale_full:
            if brand_image_grayscale_full.size > 15097152:
                raise forms.ValidationError("Please select image below 15 mb!")

        if brand_image_darkmode_full:
            if brand_image_darkmode_full.size > 15097152:
                raise forms.ValidationError("Please select image below 15 mb!")

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

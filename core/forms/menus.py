# -*- coding: utf-8 -*-
from django import forms
from core.models import Menus
import validators


# -----------------------------------------------------------------------------
# Menus
# -----------------------------------------------------------------------------
class MenusCreationForm(forms.ModelForm):
    """Custom Menus"""
    link = forms.CharField(required=False)
    parent_menu = forms.ModelChoiceField(queryset=Menus.objects.filter(parent_menu=None), required=False)

    class Meta:
        model = Menus
        exclude = ('create_by', 'create_at', 'update_at')
        labels = {
            'menu_location': 'Menu Location',
            'parent_menu': 'Parent Menu',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super(MenusCreationForm, self).clean()
        name = cleaned_data.get("name")
        link = cleaned_data.get("link")
        order = cleaned_data.get("order")
        parent_menu = cleaned_data.get("parent_menu")
        menu_location = cleaned_data.get("menu_location")

        if not name:
            raise forms.ValidationError("Please enter Title.")

        if link:
            valid = validators.url(link)
            if valid is not True:
                raise forms.ValidationError("Please enter valid link.")
        if order:
            qry = Menus.objects.filter(order=order, parent_menu=parent_menu, menu_location=menu_location)
            if qry.exists():
                raise forms.ValidationError("Please select other order for same menu.")

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance


class MenusChangeForm(forms.ModelForm):
    """Custom form to change Menus"""
    link = forms.CharField(required=False)

    class Meta:
        model = Menus
        exclude = ('create_by', 'create_at', 'update_at')
        labels = {
            'menu_location': 'Menu Location',
            'parent_menu': 'Parent Menu',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields[field].queryset = Menus.objects.filter(parent_menu=None).exclude(id=self.instance.id)

    def clean(self):
        cleaned_data = super(MenusChangeForm, self).clean()
        name = cleaned_data.get("name")
        link = cleaned_data.get("link")
        order = cleaned_data.get("order")
        parent_menu = cleaned_data.get("parent_menu")
        menu_location = cleaned_data.get("menu_location")

        if not name:
            raise forms.ValidationError("Please enter Title.")

        if link:
            valid = validators.url(link)
            if valid is not True:
                raise forms.ValidationError("Please enter valid link.")

        if order:
            qry = Menus.objects.filter(order=order, parent_menu=parent_menu, menu_location=menu_location).exclude(id=self.instance.id)
            print(qry)

            if qry.exists():
                raise forms.ValidationError("Please select other order for same menu.")

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance


# -*- coding: utf-8 -*-
from django import forms
from core.models import Pages, Review
from datetime import date

from core.models.model_changes import BikeClass


# -----------------------------------------------------------------------------
# Pages
# -----------------------------------------------------------------------------
Suspension_option = (
    ('', 'Select suspension.'),
    ('Rigid', 'Rigid'),
    ('Hardtail', 'Hardtail'),
    ('Full Suspension', 'Full Suspension'),
)

Motor_type_option = (
    ('', 'Select motor type.'),
    ('Hub', 'Hub'),
    ('Mid-Drive', 'Mid-Drive'),
)
Bike_class_option = (
    ('', 'Select Bike class.'),
    ('Class 1', 'Class 1'),
    ('Class 2', 'Class 2'),
    ('Class 3', 'Class 3'),
    ('Other', 'Other'),
)

Accessories_option = (
    ('Lights', 'Lights'),
    ('Fenders', 'Fenders'),
    ('Rack', 'Rack')
)


class PagesCreationForm(forms.ModelForm):
    """Custom Pages"""
    def _make_choices(name):
        if name == 'model_name':
            qry_review_model = Review.objects.filter(status='Published').distinct('model_name').values('model_name').order_by('model_name')
            return [(i['model_name'], i['model_name']) for i in qry_review_model]
        else:
            qry_review_model = Review.objects.filter(status='Published').exclude(trim='').distinct('trim').values('trim').order_by('trim')
            return [(i['trim'], i['trim']) for i in qry_review_model]

    slug = forms.CharField(required=False)
    min_price = forms.IntegerField(required=False, min_value=0, label='Min Price')
    max_price = forms.IntegerField(required=False, min_value=0, label='Max Price')
    min_battery_capacity = forms.IntegerField(required=False, min_value=0, label='Min Battery Capacity in Wh')
    max_battery_capacity = forms.IntegerField(required=False, min_value=0, label='Max Battery Capacity in Wh')
    min_weight = forms.IntegerField(required=False, min_value=0, label='Min Weight in lbs')
    max_weight = forms.IntegerField(required=False, min_value=0, label='Max Weight in lbs')
    meta_title = forms.CharField(required=True, label='Meta Title', widget=forms.TextInput(attrs={'placeholder': '| ElectricBikeReview.com', 'readonly': True}))
    model_name = forms.MultipleChoiceField(choices=_make_choices('model_name'), label='Model Name', required=False)
    trim = forms.MultipleChoiceField(choices=_make_choices('trim'), required=False)
    suspension = forms.ChoiceField(choices=Suspension_option, required=False)
    motor_type = forms.ChoiceField(choices=Motor_type_option, label='Motor Type', required=False)
    bike_class = forms.ChoiceField(choices=Bike_class_option, label='Bike Class', required=False)
    accessories = forms.MultipleChoiceField(choices=Accessories_option, required=False)
    # keyword = forms.ChoiceField(required=False)

    class Meta:
        model = Pages
        exclude = ('create_by', 'create_at', 'update_at')
        widgets = {
            'filter_type': forms.RadioSelect,
            'keyword': forms.TextInput(attrs={'data-role': 'tagsinput'}),
            # 'keyword': forms.SelectMultiple(attrs={'class': 'form-control', 'data-role': 'tagsinput'}),
            'min_year':forms.TextInput(attrs={'value': date.today().year-1}),
            'max_year':forms.TextInput(attrs={'value': date.today().year}),
        }
        labels = {
            'search_text': 'Basic Text Search',
            'is_filter': 'Include Filter Options',
            'filter_type': 'Filter Type',
            'page_title': 'Page Title',
            'min_year': 'Min Year',
            'max_year': 'Max Year',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['filter_type', 'is_filter']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['page_title'].widget.attrs.update({'autofocus': 'autofocus'})
        self.fields['search_text'].label = 'Basic text search'

    def clean(self):
        cleaned_data = super(PagesCreationForm, self).clean()
        name = cleaned_data.get("page_title")
        description = cleaned_data.get("description")
        min_year = cleaned_data.get("min_year")
        max_year = cleaned_data.get("max_year")
        min_price = cleaned_data.get("min_price")
        max_price = cleaned_data.get("max_price")
        min_battery_capacity = cleaned_data.get("min_battery_capacity")
        max_battery_capacity = cleaned_data.get("max_battery_capacity")
        min_weight = cleaned_data.get("min_weight")
        max_weight = cleaned_data.get("max_weight")

        if not name:
            raise forms.ValidationError("Please enter Title.")

        if not description:
            raise forms.ValidationError("Please enter Description.")

        if min_year is not None and max_year is not None:
            if int(min_year) > int(max_year):
                raise forms.ValidationError("Please max year is less then min year.")

        if min_price and max_price:
            if min_price > max_price:
                raise forms.ValidationError("Please max price is less then min price.")

        if min_battery_capacity and max_battery_capacity:
            if min_battery_capacity > max_battery_capacity:
                raise forms.ValidationError("Please max battery capacity is less then min battery capacity.")

        if min_weight and max_weight :
            if min_weight > max_weight:
                raise forms.ValidationError("Please max weight is less then min weight.")

    def save(self, commit=True):
        instance = super().save(commit=False)
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            # This is where we actually link the pizza with toppings
            instance.demo_page_bike_class.clear()
            instance.brands.clear()
            instance.categories.clear()
            bike_class_obj = BikeClass.objects.filter(bike_class=self.cleaned_data['bike_class'])
            if bike_class_obj.exists():
                instance.demo_page_bike_class.add(bike_class_obj[0])
            for brand in self.cleaned_data['brands']:
                instance.brands.add(brand)
            for category in self.cleaned_data['categories']:
                instance.categories.add(category)

        self.save_m2m = save_m2m

        if commit:
            instance.save()
            self.save_m2m()
        return instance


class PagesChangeForm(forms.ModelForm):
    """Custom form to change Pages"""

    def _make_choices(name):
        if name == 'model_name':
            qry_review_model = Review.objects.filter(status='Published').distinct('model_name').values('model_name').order_by('model_name')
            return [(i['model_name'], i['model_name']) for i in qry_review_model]
        else:
            qry_review_model = Review.objects.filter(status='Published').exclude(trim='').distinct('trim').values('trim').order_by('trim')
            return [(i['trim'], i['trim']) for i in qry_review_model]

    min_price = forms.IntegerField(required=False, min_value=0, label='Min Price')
    max_price = forms.IntegerField(required=False, min_value=0, label='Max Price')
    min_battery_capacity = forms.IntegerField(required=False, min_value=0, max_value=99999, label='Min Battery Capacity in Wh')
    max_battery_capacity = forms.IntegerField(required=False, min_value=0, max_value=99999, label='Max Battery Capacity in Wh')
    min_weight = forms.IntegerField(required=False, min_value=0, max_value=999, label='Min Weight in lbs')
    max_weight = forms.IntegerField(required=False, min_value=0, max_value=999, label='Max Weight in lbs')
    meta_title = forms.CharField(required=True, label='Meta Title', widget=forms.TextInput(attrs={'placeholder': '| ElectricBikeReview.com', 'readonly': True}))
    model_name = forms.MultipleChoiceField(choices=_make_choices('model_name'), label='Model Name', required=False)
    trim = forms.MultipleChoiceField(choices=_make_choices('trim'), required=False)
    suspension = forms.ChoiceField(choices=Suspension_option, required=False)
    motor_type = forms.ChoiceField(choices=Motor_type_option, label='Motor Type', required=False)
    bike_class = forms.ChoiceField(choices=Bike_class_option, label='Bike Class', required=False)
    accessories = forms.MultipleChoiceField(choices=Accessories_option, required=False)
    # keyword = forms.ChoiceField(required=False)

    class Meta:
        model = Pages
        exclude = ('create_by', 'create_at', 'update_at')
        widgets = {
            'filter_type': forms.RadioSelect,
            'keyword': forms.TextInput(attrs={'data-role': 'tagsinput'})
        }
        labels = {
            'search_text': 'Basic Text Search',
            'is_filter': 'Include Filter Options',
            'filter_type': 'Filter Type',
            'page_title': 'Page Title',
            'meta_title': 'Meta Title',
            'min_year': 'Min Year',
            'max_year': 'Max Year',
            'keyword': forms.TextInput(attrs={'data-role': 'tagsinput'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['filter_type', 'is_filter']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['page_title'].widget.attrs.update({'autofocus': 'autofocus'})
        self.fields['search_text'].label = 'Basic text search'
        if self.instance.model_name:
            self.initial['model_name'] = eval(self.instance.model_name)
        if self.instance.trim:
            self.initial['trim'] = eval(self.instance.trim)
        if self.instance.accessories:
            self.initial['accessories'] = eval(self.instance.accessories)

    def clean(self):
        cleaned_data = super(PagesChangeForm, self).clean()
        name = cleaned_data.get("page_title")
        description = cleaned_data.get("description")
        min_year = cleaned_data.get("min_year")
        max_year = cleaned_data.get("max_year")
        min_price = cleaned_data.get("min_price")
        max_price = cleaned_data.get("max_price")
        min_battery_capacity = cleaned_data.get("min_battery_capacity")
        max_battery_capacity = cleaned_data.get("max_battery_capacity")
        min_weight = cleaned_data.get("min_weight")
        max_weight = cleaned_data.get("max_weight")

        if not name:
            raise forms.ValidationError("Please enter Title.")

        if not description:
            raise forms.ValidationError("Please enter Description.")

        if min_year is not None and max_year is not None:
            if int(min_year) > int(max_year):
                raise forms.ValidationError("Please max year is less then min year.")

        if min_price and max_price:
            if min_price > max_price:
                raise forms.ValidationError("Please max price is less then min price.")

        if min_battery_capacity and max_battery_capacity:
            if min_battery_capacity > max_battery_capacity:
                raise forms.ValidationError("Please max battery capacity is less then min battery capacity.")

        if min_weight and max_weight:
            if min_weight > max_weight:
                raise forms.ValidationError("Please max weight is less then min weight.")

    def save(self, commit=True):
        instance = super().save(commit=False)
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            # This is where we actually link the pizza with toppings
            instance.brands.clear()
            instance.categories.clear()
            for brand in self.cleaned_data['brands']:
                instance.brands.add(brand)
            for category in self.cleaned_data['categories']:
                instance.categories.add(category)

        self.save_m2m = save_m2m

        if commit:
            self.save_m2m()
            instance.save()

        return instance


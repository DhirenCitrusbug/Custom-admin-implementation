# -*- coding: utf-8 -*-
from django import forms
from core.models import Comments, Review, ReviewBrand, ReviewCategory, Pages
from core.utils import send_reply_mail


# -----------------------------------------------------------------------------
# Comments
# -----------------------------------------------------------------------------
class CommentsCreationForm(forms.ModelForm):
    """Custom Comments"""
    class Meta:
        model = Comments
        fields = ['name', 'email', 'ip', 'description', 'is_approved']
        # exclude = ('create_at', 'update_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    # def clean(self):
    #     cleaned_data = super(CommentsCreationForm, self).clean()
        # parent_id = cleaned_data.get('parent_id')
        # if parent_id is None:
        #     raise forms.ValidationError("Please parent comment not found.")

    def save(self, commit=True):
        instance = super().save(commit=False)
        domain = 'http://54.213.76.238'
        if commit:
            instance.save()
            if instance.parent_id is not None:
                    if instance.parent_id.is_notification:
                        context_type = instance.comment_type
                        comment_type_id = instance.comment_type_id
                        url = None
                        if context_type == 'Review':
                            qry_review = Review.objects.filter(id=comment_type_id)
                            if qry_review.exists():
                                url = 'http://{}/{}/{}/'.format(domain, qry_review[0].brands.all()[0].slug, qry_review[0].slug)
                        elif context_type == 'Brand':
                            qry_review_brand = ReviewBrand.objects.filter(id=comment_type_id)
                            if qry_review_brand.exists():
                                url = 'http://{}/brand/{}/'.format(domain, qry_review_brand[0].slug)
                        elif context_type == 'Category':
                            qry_review_category = ReviewCategory.objects.filter(id=comment_type_id)
                            if qry_review_category.exists():
                                url = 'http://{}/category/{}/'.format(domain, qry_review_category[0].slug)
                        elif context_type == 'Custom_Landing':
                            qry_page = Pages.objects.filter(id=comment_type_id)
                            if qry_page.exists():
                                url = 'http://{}/{}/'.format(domain, qry_page[0].slug)

                        # Use below function for send comment id.
                        # send_reply_mail(instance, url)

                        unsubscribe_url = '{}/customadmin/unsubscribe/{}'.format(domain, instance.parent_id.id)
                        send_reply_mail(instance, unsubscribe_url)

        return instance


class CommentsChangeForm(forms.ModelForm):
    """Custom Comments"""
    class Meta:
        model = Comments
        fields = ['name', 'email', 'description', 'is_approved']
        exclude = ('create_at', 'update_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super(CommentsChangeForm, self).clean()
        name = cleaned_data.get("name")
        # email = cleaned_data.get("email")
        description = cleaned_data.get("description")

        # if not name:
        #     raise forms.ValidationError("Please enter name.")

        if not description:
            raise forms.ValidationError("Please enter description.")

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance

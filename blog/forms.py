from django import forms
from .models import Posts
from tinymce import TinyMCE


class PostForm(forms.Form):
    content = forms.CharField(
        widget=TinyMCE(attrs={
            'required': False,
            'cols': 30,
            'rows': 10
        }))

    # class Meta:
    #     model = Posts
    #     fields = '__all__'

class PrivacyPolicyForm(forms.Form):
    content = forms.CharField(
        widget=TinyMCE(attrs={
            'required': False,
            'cols': 30,
            'rows': 10
        }))

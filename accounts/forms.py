from django import forms
from .models import UserInfo

class AddBioForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['bio']
from dataclasses import fields
from django import forms
from ContractRecord.models import *

User = get_user_model()


class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True

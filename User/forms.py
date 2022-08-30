from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class StaffUserForm(forms.ModelForm):
    password = forms.CharField(label='رمز عبور', required=True)

    class Meta:
        model = User
        fields = [
            'firstName',
            'lastName',
            'phone',
            'national_id',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['password'].required = False

    def save(self, commit=True):
        password = self.cleaned_data.pop('password', None)
        obj = super().save(False)

        if password:
            obj.set_password(password)

        obj.is_staff = True
        obj.is_active = True
        obj.save()
        return obj


class UserUploadDocumentsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True

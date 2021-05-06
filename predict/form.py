from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    fullname = forms.CharField(label = "First name")

    class Meta:
        model = User
	def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        first_name, last_name = self.cleaned_data["fullname"].split()
        user.first_name = first_name
        user.last_name = last_name
        if commit:
            user.save()
        return user
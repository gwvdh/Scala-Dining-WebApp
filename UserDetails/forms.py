from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.utils import OperationalError
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from Dining.models import UserDiningSettings
from .models import User, Association, UserMembership


class RegisterUserForm(UserCreationForm):
    password2 = forms.CharField(widget=forms.PasswordInput, label="Password confirmation")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')

    def clean_email(self):
        cleaned_email = self.cleaned_data['email']
        if User.objects.filter(email=cleaned_email).exists():
            msg = 'E-mail is already used. Did you forget your password?'
            raise ValidationError(msg)
        return cleaned_email


class RegisterUserDetails(forms.ModelForm):
    first_name = forms.CharField(max_length=40, required=True)
    last_name = forms.CharField(max_length=40, required=True)
    allergies = forms.CharField(max_length=100, required=False, help_text="Max 100 characters, leave empty if none")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'allergies']

    def save_as(self, user):
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.userdiningsettings.allergies = self.cleaned_data.get('allergies')
        user.save()
        user.userdiningsettings.save()


class RegisterAssociationLinks(forms.Form):
    # Todo? Could change the widget to e.g. checkboxes
    try:
        associations = forms.MultipleChoiceField(
            choices=[(a.pk, a.name) for a in Association.objects.filter(is_choosable=True)],
            help_text='At which associations are you active?')
        # In case associations table did not exist yet, except the operation
    except OperationalError:
        pass

    def create_links_for(self, user):
        for association in self.cleaned_data['associations']:
            UserMembership.objects.create(related_user=user, association_id=association)


class DiningProfileForm(ModelForm):
    class Meta:
        model = UserDiningSettings
        fields = ['allergies']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].disabled = True
        self.fields['last_name'].disabled = True
        self.fields['email'].disabled = True

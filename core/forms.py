from allauth.account.forms import LoginForm,SignupForm
from django import forms
from django.utils.translation import gettext, gettext_lazy as _, pgettext
from phone_field import PhoneFormField
from .models import Profile

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args,**kwargs)
        self.fields['login'].widget.attrs.update({
            'class':'form-login'
        })
        self.fields['remember'].widget.attrs.update({
            'class':'remember-login'
        })


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(label=_("First Name"),
                                    max_length=20,
                                    widget=forms.TextInput(
                                    attrs={'placeholder':
                                            _('First Name'),
                                            'autofocus': 'autofocus'}))
    last_name = forms.CharField(label=_("Last Name"),
                                max_length=20,
                                widget=forms.TextInput(
                                    attrs={'placeholder':
                                            _('Last Name')}))
    phone_nmbr = PhoneFormField()
    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        return user
    














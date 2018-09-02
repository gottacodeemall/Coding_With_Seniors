from collections import OrderedDict

from django import forms
from django.contrib.auth.models import User

from user_profile.models import UserProfile
from user_profile.models import Site_user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['display_name', 'display_pic', 'reg_number','bio']
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['display_pic'].label = "URL to the photo -> http://giphy.com/"
        self.fields['display_pic'].widget.attrs.update({
            'class': 'form-control validate',
        })

        self.fields['display_name'].label = 'Display Name'
        self.fields['display_name'].widget.attrs.update({
            'class': 'form-control validate',
        })
        self.fields['display_name'].required=True

        self.fields['reg_number'].label = 'NITC Registration Number-in CAPITALS'
        self.fields['reg_number'].widget.attrs.update({
            'class': 'form-control validate',
        })
        self.fields['reg_number'].required = True

        self.fields['bio'].label = 'Short Description/Tag Line'
        self.fields['bio'].widget.attrs.update({
            'class': 'form-control validate',
        })


class UserForm(forms.ModelForm):
    password_validation = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        #remove redundancy by declaring things here rather refer them to model.
        #https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/
        #Model Forms have another kwarg, instance, that holds the instance we’re editing.
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        #https://stackoverflow.com/questions/19197684/clarification-when-where-to-use-super-in-django-python
        #why super- super gives parent objects
        self.fields['username'].label = 'Username (Format: firstname_lastname)'
        self.fields['username'].widget.attrs.update({
            'class': 'form-control validate',
        })

        self.fields['email'].label = 'User email'
        self.fields['email'].widget = forms.EmailInput()
        self.fields['email'].widget.attrs.update({
            'class': 'form-control validate',
        })

        self.fields['password'].label = 'Password'
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs.update({
            'class': 'form-control validate',
        })

        self.fields['password_validation'].label = 'Password verification'
        self.fields['password_validation'].widget = forms.PasswordInput()
        self.fields['password_validation'].widget.attrs.update({
            'class': 'form-control validate',
        })
        #if the password has already been set or user registered already.
        if self.instance.pk is not None:
            self.fields['password_validation'].required = False
            self.fields['password_validation'].label = 'New password verification'
            self.fields['password'].required = False
            self.fields['password'].label = 'New password'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('An email is required')
        elif (self.instance and User.objects.filter(email=email).exclude(id=self.instance.id).count() != 0) or \
                (not self.instance and User.objects.filter(email=email).count() != 0):
            raise forms.ValidationError('An account using this email already exists.')
        return email

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        password_validation = cleaned_data.get("password_validation")
        if password or password_validation:
            if password_validation != password:
                error = "Passwords don't match."
                raise forms.ValidationError(error)
        return cleaned_data


class LoginForm(forms.Form):
    username_or_email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username_or_email'].label = 'Username or email'
        self.fields['username_or_email'].widget.attrs.update({
            'class': 'form-control validate',
        })

        self.fields['password'].label = 'Password'
        self.fields['password'].widget.attrs.update({
            'class': 'form-control validate'
        })


class CodingAccountForm(forms.ModelForm):
    class Meta:
        model = Site_user
        fields = ['username_on_site','sites','url']
    def __init__(self, *args, **kwargs):
        super(CodingAccountForm, self).__init__(*args, **kwargs)
        self.fields['username_on_site'].label = 'Username on platform'
        self.fields['username_on_site'].widget.attrs.update({
            'class': 'form-control validate',
        })
        self.fields['url'].label = 'url'
        self.fields['url'].widget.attrs.update({
            'class': 'form-control validate',
        })

        self.fields['sites'].label = 'Platform'
        self.fields['sites'].widget.attrs.update({
            'class': 'form-control validate',
        })
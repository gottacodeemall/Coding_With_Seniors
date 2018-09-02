from collections import OrderedDict

from django import forms
from django.contrib.auth.models import User
from django.contrib.admin import widgets

from events.models import Editorial

class AddEditorialForm(forms.ModelForm):
    class Meta:
        model = Editorial
        fields = ['name','solution','solution_url']
    def __init__(self, *args, **kwargs):
        super(AddEditorialForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Name of the Editorial (Format: Problem_Name-Display_Name)"
        self.fields['name'].widget.attrs.update({
            'class': 'form-control validate',
        })

        self.fields['solution'].label = 'Approach taken for Solution'
        self.fields['solution'].widget.attrs.update({
            'class': 'form-control validate',
        })

        self.fields['solution_url'].label = 'Link to the code'
        self.fields['solution_url'].widget.attrs.update({
            'class': 'form-control validate',
        })




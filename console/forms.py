from collections import OrderedDict

from django import forms
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from events.models import Event,Session,Problem,Ranking,ReadingMaterial

class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'description']
    def __init__(self, *args, **kwargs):
        super(AddEventForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Name"
        self.fields['name'].widget.attrs.update({
            'class': 'form-control validate',
        })

        self.fields['date'].label = 'Date(yyyy-mm-dd)'
        self.fields['date'].widget.attrs.update({
            'class': 'form-control validate date-input',
        })

        self.fields['description'].label = 'Description'
        self.fields['description'].widget.attrs.update({
            'class': 'form-control validate',
        })

class AddProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['name', 'url_problem', 'solution','url_solution','tags']
    def __init__(self, *args, **kwargs):
        super(AddProblemForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Name/ID"
        self.fields['name'].widget.attrs.update({
            'class': 'form-control validate',
        })
        self.fields['url_problem'].label = 'URL problem'
        self.fields['url_problem'].widget.attrs.update({
            'class': 'form-control validate date-input',
        })
        self.fields['solution'].label = 'Solution Name'
        self.fields['solution'].widget.attrs.update({
            'class': 'form-control validate date-input',
        })
        self.fields['url_solution'].label = 'Solution URL'
        self.fields['url_solution'].widget.attrs.update({
            'class': 'form-control validate date-input',
        })

        self.fields['tags'].label = 'Tag(use ctrl+click for multiple tags)'
        self.fields['tags'].widget.attrs.update({
            'class': 'form-control validate',
        })



class AddSessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['name', 'date','description','test_name','test_url']
    def __init__(self, *args, **kwargs):
        super(AddSessionForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Name"
        self.fields['name'].widget.attrs.update({
            'class': 'form-control validate',
        })
        self.fields['date'].label = 'Date(yyyy-mm-dd)'
        self.fields['date'].widget.attrs.update({
            'class': 'form-control validate date-input',
        })
        self.fields['description'].label = 'Description'
        self.fields['description'].widget.attrs.update({
            'class': 'form-control validate',
        })
        self.fields['test_name'].label = 'Name of contest'
        self.fields['test_name'].widget.attrs.update({
            'class': 'form-control validate',
        })
        self.fields['test_url'].label = 'Contest URL'
        self.fields['test_url'].widget.attrs.update({
            'class': 'form-control validate',
        })

class RankForm(forms.ModelForm):
    class Meta:
        model = Ranking
        fields = ['rank','user']
    def __init__(self, *args, **kwargs):
        super(RankForm, self).__init__(*args, **kwargs)
        self.fields['rank'].label = 'Rank'
        self.fields['rank'].widget.attrs.update({
            'class': 'form-control validate',
        })
        self.fields['user'].label = "User"
        self.fields['user'].widget.attrs.update({
            'class': 'form-control validate',
        })

class AddReadingForm(forms.ModelForm):
    class Meta:
        model = ReadingMaterial
        fields = ['name','url','type']
    def __init__(self, *args, **kwargs):
        super(AddReadingForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Name'
        self.fields['name'].widget.attrs.update({
            'class': 'form-control validate',
        })
        self.fields['url'].label = "Link to material"
        self.fields['url'].widget.attrs.update({
            'class': 'form-control validate',
        })
        self.fields['type'].label = "Type(Reading/Video/anything)"
        self.fields['type'].widget.attrs.update({
            'class': 'form-control validate',
        })




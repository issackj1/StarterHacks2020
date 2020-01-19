from django import forms

class Data(forms.Form):
    name = forms.CharField(name='name', max_length=100)
    email = forms.CharField(name='email')
    cweight = forms.CharField(name='cweight')
    dweight = forms.CharField(name='dweight')
    age = forms.CharField(name='age')
    sex = forms.CharField(name='sex')
    height = forms.CharField(name='height')

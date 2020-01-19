from django import forms

class RegisterForm(forms.Form):
    user = forms.CharField()
    email = forms.EmailField()
    cweight = forms.CharField()
    dweight = forms.CharField()
    age = forms.CharField()
    sex = forms.CharField()
    height = forms.CharField()

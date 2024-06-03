from django import forms 


class TextInputForm(forms.Form):
    input = forms.CharField(max_length=32, required=False)

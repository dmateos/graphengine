from django import forms


class InputForm(forms.Form):
    input = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))

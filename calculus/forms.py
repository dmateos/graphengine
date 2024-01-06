from django import forms


class TextInputForm(forms.Form):
    input = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))


class ImageInputForm(forms.Form):
    input = forms.ImageField()

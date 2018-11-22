from django import forms
from .models import commentModel
class EmailsendForm(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    to=forms.EmailField()
    comments=forms.CharField(required=False,widget=forms.Textarea)
class commentForm(forms.ModelForm):
    class Meta:
        model=commentModel
        fields=('name','email','body')

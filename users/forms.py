from django import forms
from users.models import ClientUser

class LoginForm(forms.Form):
    club_premier_id = forms.CharField(max_length=16, required=True)
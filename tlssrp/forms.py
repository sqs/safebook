import base64

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, UNUSABLE_PASSWORD
from django import forms

from safebook.tlssrp.models import SRPUserInfo, srpb64encode

class SRPVerifierInput(forms.TextInput):
    input_type = 'srp-verifier'

class SRPSaltInput(forms.TextInput):
    input_type = 'srp-salt'

class SRPUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and password.
    """
    username = forms.RegexField(label="Username", max_length=30, regex=r'^[a-zA-Z0-9]+$',
        error_messages = {'invalid': "This value may contain only [a-zA-Z0-9]."})
    verifier = forms.CharField(label="SRP verifier", widget=SRPVerifierInput)
    salt     = forms.CharField(label="SRP salt", widget=SRPSaltInput)
    group_index = forms.ChoiceField(label="SRP group size (bits)",
                                   choices=((1,'1024'), (2,'1536'), (3,'2048')))

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("A user with that username already exists.")

    def clean_salt(self):
        return srpb64encode(base64.b64decode(self.cleaned_data['salt']))

    def clean_verifier(self):
        return srpb64encode(base64.b64decode(self.cleaned_data['verifier']))
    
    def save(self, commit=True):
        user = super(SRPUserCreationForm, self).save(commit=False)
        user.password = UNUSABLE_PASSWORD
        srpinfo = SRPUserInfo()
        srpinfo.verifier = self.cleaned_data['verifier']
        srpinfo.salt     = self.cleaned_data['salt']
        srpinfo.group_index = self.cleaned_data['group_index']
        if commit:
            user.save()
            srpinfo.user = user
            srpinfo.save()
        return user

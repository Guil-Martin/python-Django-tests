from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Overrides the form UserCreationForm used in app.templates.register_user
class  CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class':'form-control', 'name':'usernamel', 'placeholder':'Enter username...'})
        self.fields['password1'].widget.attrs.update(
            {'class':'form-control', 'name':'password1', 'placeholder':'Enter password...'})
        self.fields['password2'].widget.attrs.update(
            {'class':'form-control', 'name':'password2', 'placeholder':'Confirm password...'})
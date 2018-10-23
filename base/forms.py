from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class TodoForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

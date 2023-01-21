from django import forms
from app.models import User, Profile
from django.core.exceptions import ValidationError
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import auth


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SettingsUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Password confirmation")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New password if need", required=False)
    password_check = forms.CharField(widget=forms.PasswordInput, label="Repeat password", required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def clean_password_check(self):
        new_password = self.cleaned_data['new_password']
        password_for_checking = self.cleaned_data['password_check']
        if password_for_checking != new_password:
            raise ValidationError("Passwords don't match!")
        return password_for_checking
    
    def update(self, user):
        data = self.cleaned_data

        username = data['username']
        password = data['password']
        new_password = data['new_password']

        data.pop('username')
        data.pop('password')
        data.pop('new_password')
        data.pop('password_check')

        User.objects.filter(username=username).update(**data)

        user_tmp = User.objects.get(username=username)
        if new_password != "":
            user_tmp.set_password(new_password)
            user_tmp.save()
        return user_tmp


class SettingsProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
    
    def update(self, user):
        return Profile.objects.filter(user_id=user.id).update(user=user, **self.cleaned_data)


class SignUpUserForm(forms.ModelForm):
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput
        }
    
    def clean_password_check(self):
        password = self.cleaned_data['password']
        password_for_checking = self.cleaned_data['password_check']
        if password_for_checking != password:
            raise ValidationError("Passwords don't match!")
        return password_for_checking
    
    def save(self):
        data = self.cleaned_data
        data.pop('password_check')
        return User.objects.create_user(**data)


class SignUpProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
    
    def save(self, user):
        return Profile.objects.create(user=user, **self.cleaned_data)

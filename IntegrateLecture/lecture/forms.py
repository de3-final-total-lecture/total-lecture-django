from django import forms
from .models import Users
from .choices import LANGUAGE_CHOICES, SKILL_CHOICES
from django.contrib.auth.forms import AuthenticationForm

class CustomSignUpForm(forms.ModelForm):
    password_1 = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(widget=forms.PasswordInput)
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES, required=True)
    skill_1 = forms.ChoiceField(choices=SKILL_CHOICES, required=False)
    skill_2 = forms.ChoiceField(choices=SKILL_CHOICES, required=False)

    class Meta:
        model = Users
        fields = ['user_name', 'user_email', 'password_1', 'password_2', 'language', 'skill_1', 'skill_2']

    def password_validation(self):
        password_1 = self.cleaned_data.get('password_1')
        if len(password_1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if len(password_1) > 16:
            raise forms.ValidationError("Password must be no more than 16 characters long.")
        if not any(char.isupper() for char in password_1):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in password_1):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        if not any(char.isdigit() for char in password_1):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not any(char in '!@#$%^&*()-_=+[]{}|;:,.<>?' for char in password_1):
            raise forms.ValidationError("Password must contain at least one special character.")
        return password_1

    def clean(self):
        cleaned_data = super().clean()
        password_1 = cleaned_data.get("password_1")
        password_2 = cleaned_data.get("password_2")

        if password_1 and password_2 and password_1 != password_2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password_1"])
        
        skills = {
            self.cleaned_data['language']: 8
        }
        if self.cleaned_data.get('skill_1'):
            skills[self.cleaned_data['skill_1']] = 4
        if self.cleaned_data.get('skill_2'):
            skills[self.cleaned_data['skill_2']] = 4
        
        # sorted_skills = dict(sorted(skills.items(), key=lambda item: item[1], reverse=True))
        
        user.skills = skills
        if commit:
            user.save()
        return user
        

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['user_name', 'github_url', 'linkedin_url'] # 이후 선별하여 추가 예정
        widgets = {
            'github_url': forms.URLInput(attrs={'required': False}),
            'linkedin_url': forms.URLInput(attrs={'required': False}),
        }
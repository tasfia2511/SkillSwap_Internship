from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile


# ============================================================
# PROFILE FORM
# ============================================================

class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile

        fields = [
            'bio',
            'skills_have',
            'skills_want',
        ]

        widgets = {

            'bio': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': (
                        'Tell others a little about yourself...'
                    ),
                }
            ),

            'skills_have': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': (
                        'Example: Python, Django, Photoshop'
                    ),
                }
            ),

            'skills_want': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': (
                        'Example: React, Spanish, Photography'
                    ),
                }
            ),
        }


# ============================================================
# SIGN UP FORM
# ============================================================

class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
                'autocomplete': 'email',
            }
        )
    )

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username',
                'autocomplete': 'username',
            }
        )
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Create a password',
                'autocomplete': 'new-password',
            }
        )
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm your password',
                'autocomplete': 'new-password',
            }
        )
    )

    class Meta:

        model = User

        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )

    def save(self, commit=True):

        user = super().save(commit=False)

        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


# ============================================================
# USER PROFILE FORM
# ============================================================

class UserProfileForm(forms.ModelForm):

    class Meta:

        model = UserProfile

        fields = [
            'bio',
            'skills_have',
            'skills_want',
        ]

        widgets = {

            'bio': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': (
                        'Tell others about yourself...'
                    ),
                }
            ),

            'skills_have': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': (
                        'Example: Python, Django, C++'
                    ),
                }
            ),

            'skills_want': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': (
                        'Example: React, Node.js, Spanish'
                    ),
                }
            ),
        }


# ============================================================
# USER ACCOUNT UPDATE FORM
# ============================================================

class UserUpdateForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]

        widgets = {

            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                }
            ),

            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }
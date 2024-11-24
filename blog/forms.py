from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from .models import Comment, User, Author

from pprint import pprint



class LoginForm(forms.Form):
    credential = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['credential'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username or Email',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
        })

    def add_error(self, field, error):
        if field:
            self.fields[field].widget.attrs['class'] += ' border-red-500'
        else:
            self.non_field_errors().append(error)

    def non_field_errors(self):
        if not hasattr(self, '_non_field_errors'):
            self._non_field_errors = []
        return self._non_field_errors

    def clean(self):
        cleaned_data = super().clean()
        credential = cleaned_data.get('credential')
        password = cleaned_data.get('password')

        try:
            user = User.objects.get(email=credential)
        except User.DoesNotExist:
            pprint('Error')
            try:
                user = User.objects.get(username=credential)
            except User.DoesNotExist:
                self.add_error(None, 'Invalid credentials')
                return

        if not user.check_password(password):
            self.add_error(None, 'Invalid credentials')
            return

        if not user:
            self.add_error(None, 'Invalid credentials')
            return

        self.cleaned_data['user'] = user
        self.user = user

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'password': 'Password',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',
        })
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'First Name',
        })
        self.fields['last_name'].required = True
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Last Name',
        })
        self.fields['email'].required = True
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
        })

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except forms.ValidationError as e:
            self.add_error('password', e)
            return
        hash_password = make_password(password)
        return hash_password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        labels = {'body': ''}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Add a comment...',
            'rows': '3',
            'cols': '65',
        })
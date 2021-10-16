from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

User = get_user_model()


#   #   ###   #   ###   #   #       register first method: class base  ##   #   #   #   #####  #  #   ###   #
class RegistrationForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError(_('username already exists'))

        if User.objects.filter(email=self.cleaned_data["email"]).exists():
            raise forms.ValidationError(_("email already exists"))
        return self.cleaned_data

    def save(self):
        user = User.objects.create_user(**self.cleaned_data)
        return user


#   #   #  #   #   #   #  #   #   # #    register second method: function base #   # #   #   #  #   #   #   #  #   #
def forbidden_users(value):
    forbidden_user = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root',
                      'email', 'user', 'join', 'sql', 'static', 'python', 'delete']
    if value.lower() in forbidden_user:
        raise ValidationError('Invalid name for user, this is a reserved word.')


def invalid_user(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('This is an Invalid user, Do not user these chars: @ , - , + ')


def unique_email(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this email already exists.')


def unique_user(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('User with this username already exists.')


class SignupForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(), max_length=30, required=True, )
    email = forms.CharField(widget=forms.EmailInput(), max_length=100, required=True, )
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label="Confirm your password.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].validators.append(forbidden_users)
        self.fields['username'].validators.append(invalid_user)
        self.fields['username'].validators.append(unique_user)
        self.fields['email'].validators.append(unique_email)

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            self._errors['password'] = self.error_class(['Passwords do not match. Try again'])
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=12, widget=forms.PasswordInput)

    def clean(self):
        user = User.objects.filter(username=self.cleaned_data["username"]).first()
        if user is None:
            raise ValueError(_("this username does not exists"))

        user = authenticate(**self.cleaned_data)
        if user is None:
            raise forms.ValidationError(_("Unable login with provided credentials"))
        self.cleaned_data['user'] = user
        return self.cleaned_data


class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="Old password",
                                   required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="New password",
                                   required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}),
                                       label="Confirm new password", required=True)

    class Meta:
        model = User
        fields = ('id', 'old_password', 'new_password', 'confirm_password')

    def clean(self):
        super(ChangePasswordForm, self).clean()
        id = self.cleaned_data.get('id')
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        user = User.objects.get(pk=id)
        if not user.check_password(old_password):
            self._errors['old_password'] = self.error_class(['Old password do not match.'])
        if new_password != confirm_password:
            self._errors['new_password'] = self.error_class(['Passwords do not match.'])
        return self.cleaned_data


class EditProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    username = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
    url = forms.URLField(widget=forms.TextInput(), max_length=60, required=False)
    bio = forms.CharField(widget=forms.TextInput(), max_length=260, required=False)

    class Meta:
        model = User
        fields = ('avatar', 'username', 'bio')

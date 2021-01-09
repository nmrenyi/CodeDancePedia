"""Forms for users
    By Liu Chang
"""


from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from manage_user.models import User


class UserCreateForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
        fields, plus a repeated password.
    """
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    password_confirm = forms.CharField(
        label="password_confirm",
        widget=forms.PasswordInput,
    )

    class Meta:
        """Meta class for UserCreateForm

        """
        model = User
        fields = '__all__'

    def clean_password_confirm(self):
        """Validate password confirm

        Returns:

        """
        # check the two passwords
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        print("-----"+str(password))
        print("-----"+str(password_confirm))
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords don't match")
        return password_confirm

    def save(self, commit=True):
        """Save changes to user info

        Args:
            commit:

        Returns:

        """
        # save the provided password in hashed format
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on
       the user, but replaces the password field with admin's
       password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        """Meta class for UserChangeForm
        """
        model = User
        fields = '__all__'

    def clean_password(self):
        """Validate password

        Returns:
            initial password
        """
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial['password']

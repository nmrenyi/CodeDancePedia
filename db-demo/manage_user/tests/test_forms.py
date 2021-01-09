"""Test file for manage_user forms.py
    By Liu Chang
"""
import pytest
from django.test import TestCase
from django import forms

from manage_user.forms import UserCreateForm, UserChangeForm
from manage_user.models import User


@pytest.fixture(scope="function")
def users():
    """Generate user fixture

    Returns:
        user_list
    """
    user_list = [
        {
            "password": "123456",
            "password_confirm": "123456"
        },
        {
            "password": "123456",
            "password_confirm": "123457"
        }
    ]
    return user_list


class UserCreateFormTest(TestCase):
    """Test User Create Form
    """
    def setUp(self) -> None:
        """Set up database

        Returns:

        """
        User.objects.create(username="user1", password="123456",
                            email="CodeDance@mails.tsinghua.edu.cn", is_admin=False)
        User.objects.create(username="user2", password="asdfg",
                            email="code@gmail.com", is_admin=False)

    def test_valid(self):
        """Test valid user

        Returns:

        """
        form = UserCreateForm(data={
                                    "username": "user4",
                                    "password": "123456",
                                    "password_confirm": "123456",
                                    "email": "CodeDance@mails.tsinghua.edu.cn"
                                })
        print(form.is_valid())
        # self.assertTrue(form.is_valid())
        print(form.clean_password_confirm())
        self.assertEqual(form.clean_password_confirm(), "123456")

    def test_invalid(self):
        """Test invalid user

        Returns:

        """
        form = UserCreateForm(data=
                              {
                                  "username": "user5",
                                  "password": "12345",
                                  "password_confirm": "123457",
                                  "email": "user5@gmail.com"})
        if form.is_valid():
            with self.assertRaises(forms.ValidationError):
                form.clean_password_confirm()

    def test_save(self):
        """Test save form

        Returns:

        """
        form = UserCreateForm(data=
                              {"username": "user3",
                               "password": "qwerty",
                               "password_confirm": "qwerty",
                               "email": "user3@gmail.com"})
        print(form.is_valid())
        self.assertIsNotNone(form.save())


class UserChangeFormTest(TestCase):
    """Test User Change Form
    """
    def setUp(self) -> None:
        """Set up database

        Returns:

        """
        self.user1 = User.objects.create(username="user1", password="123456",
                                         email="CodeDance@mails.tsinghua.edu.cn", is_admin=False)
        self.user2 = User.objects.create(username="user2", password="asdfg",
                                         email="code@gmail.com", is_admin=False)

    def test_clean_password(self):
        """Test validating password

        Returns:

        """
        form = UserChangeForm(data={"username": "user1", "password_confirm": "123456",
                                    "email": "CodeDance@mails.tsinghua.edu.cn"},
                              initial={"password": "qwerty"})
        # self.assertEqual(form.clean_password_confirm(), "123456")
        print(form.clean_password())
        self.assertIsNotNone(form.clean_password())
        self.assertEqual(form.clean_password(), "qwerty")

"""Test file for manage_user admin.py
    By Liu Chang
"""
import pytest


@pytest.mark.django_db
def test_admin_login(admin_client):
    """Test admin login

    Returns:

    """
    response = admin_client.get('/admin/')
    assert response.status_code == 200

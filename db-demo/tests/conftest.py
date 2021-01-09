"""Config pytest fixture
    By Liu Chang
"""
import pytest
from django.core.management import call_command

# @pytest.fixture(scope='session')
# def django_db_modify_db_settings():
#     """
#     Modify default settings of database, to support connection with mysql
#     """
#


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker, django_db_modify_db_settings):
    """

    Args:
        django_db_blocker ([type]): [description]
    """
    with django_db_blocker.unblock():
        call_command('loaddata', 'test_docs.json')

"""Urls for manage_user app
    By Liu Chang
"""


from django.conf.urls import url
from .views import register, login, get_history, get_info

urlpatterns = [
    url(r'^register/', register),
    url(r'^login/', login),
    url(r'^history', get_history),
    url(r'^info', get_info),
]

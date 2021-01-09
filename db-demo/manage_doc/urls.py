'''
url router for manage_doc app
By LiuChang, RenYi
'''
from django.conf.urls import url
from .views import show_all
from .views import search, add
from .views import upload, modify

urlpatterns = [
    url(r'^all/', show_all),
    url(r'search/', search),
    url(r'add/', add),
    url(r'upload/', upload),
    url(r'modify/', modify),
]

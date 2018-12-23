from django.urls import path, re_path
from . import views

app_name = 'puzzle'

urlpatterns = [
    re_path(r'^puzzle/add/$', views.add_puzzle, name = 'add'),
    re_path(r'^puzzle/(?P<puzzid>\w+)/$', views.puzzle, name = 'puzzle'),
]

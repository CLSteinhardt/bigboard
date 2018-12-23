from django.urls import include, path, re_path
from . import views

app_name = 'hunts'

urlpatterns = [
    re_path(r'^hunts/add/$', views.add_hunt, name = 'add'),
    re_path(r'^hunts/$', views.all_hunts, name = 'all'),
    re_path(r'^/$', views.all_hunts, name = 'all'),
    re_path(r'^hunt/(?P<huntid>\w+)/$', views.hunt, name = 'hunt'),
    re_path(r'^', include('puzzle.urls')),
]

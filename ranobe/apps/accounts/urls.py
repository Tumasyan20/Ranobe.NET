from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^(?P<current_user_id>\d+)$', views.profile_detail, name = 'user-detail'),
]
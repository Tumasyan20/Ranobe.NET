from django.conf.urls import url
from django.urls import path
from . import views


# Create your views here.

urlpatterns = [
	url(r'^books/$', views.Book_list, name = 'books'),
    url(r'^book/(?P<book_id>\d+)$', views.book_detail, name = 'book-detail'),
    url(r'^book/(?P<book_id>\d+)/chapter/(?P<chapter_id>\d+)$', views.chapter_detail, name = "chapter-detail"),
]
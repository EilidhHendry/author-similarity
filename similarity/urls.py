from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^all_chunks$', views.all_chunks, name='all_chunks'),
    url(r'^classify$', views.classify, name='classify'),
]

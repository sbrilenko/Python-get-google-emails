from django.conf.urls import url
from emails import views as emails_views
from . import views


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^logout/$', views.logout_user, name="logout"),
    url(r'^emails/', emails_views.Emails.as_view(), name='emails'),
]
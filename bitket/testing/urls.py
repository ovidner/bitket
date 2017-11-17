from django.conf.urls import url

from .views import FakeAuthorizationView


urlpatterns = [
    url(r'^oauth/authorization/(?P<provider>[\w-]+)/(?P<key>[\w-]+)/$', FakeAuthorizationView.as_view())
]

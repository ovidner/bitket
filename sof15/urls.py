from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from tickle.views.people import LoginView, ProfileView
from orchard.views import ApproveOrchestraMemberView, RegisterOrchestraMemberView

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'sof15.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', TemplateView.as_view(template_name='base.html')),

    url(r'^people/login/$', LoginView.as_view(), name='login'),
    url(r'^people/(?P<pk>\d+)/$', ProfileView.as_view(), name='profile'),
    url(r'^people/me/$', LoginView.as_view(), name='profile_me'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^karthago/', include('karthago.urls', namespace='karthago', app_name='karthago')),
    url(r'^orchard/', include('orchard.urls', namespace='orchard', app_name='orchard')),

    #url(r'^people/', )
)

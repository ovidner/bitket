from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from orchard.views import ApproveOrchestraMemberView, RegisterOrchestraMemberView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sof15.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='base.html')),

    url(r'^karthago/', include('karthago.urls')),

    url(r'^orchard/(?P<pk>\d+)/$', ApproveOrchestraMemberView.as_view(), name='approve_orchestra_members'),
    url(r'^orchard/members/add/$', RegisterOrchestraMemberView.as_view(), name='register_orchestra_member'),
    url(r'^orchard/members/add/success/$', TemplateView.as_view(template_name='orchard/register_complete.html'), name='register_orchestra_member_success'),

    )

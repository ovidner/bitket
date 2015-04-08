from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from tickle.views.people import LoginView, ProfileView, ChangePasswordView, CreateUserView,\
from orchard.views import ApproveOrchestraMemberView, RegisterOrchestraMemberView
from fungus.views import ShiftChangeView

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'sof15.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', TemplateView.as_view(template_name='base.html'), name='root'),

    url(r'^people/login/$', LoginView.as_view(), name='login'),
    url(r'^people/change-password/$', ChangePasswordView.as_view(), name='change_password'),
    url(r'^people/create-account/$', CreateUserView.as_view(), name='create_user'),
    url(r'^people/create-account/success$', TemplateView.as_view(template_name='people/create_user_success.html'),
        name='create_user_success'),
    url(r'^people/logout/$', 'django.contrib.auth.views.logout', {'next_page': 'root'}, name='logout'),
    url(r'^people/(?P<pk>\d+)/$', ProfileView.as_view(), name='profile'),
    url(r'^people/me/$', LoginView.as_view(), name='profile_me'),

    url(r'^admin/fungus/shiftregistration/shifchange/$', ShiftChangeView.as_view(), name='change_selected_shifts'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^karthago/', include('karthago.urls', namespace='karthago', app_name='karthago')),
    url(r'^orchard/', include('orchard.urls', namespace='orchard', app_name='orchard')),
    url(r'^fungus/', include('fungus.urls', namespace='fungus', app_name='fungus')),

    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)

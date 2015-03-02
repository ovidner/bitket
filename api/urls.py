# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from fungus.api import views

router = routers.DefaultRouter()
router.register(r'shifts', views.ShiftViewSet)
router.register(r'shift-registrations', views.ShiftRegistrationViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]

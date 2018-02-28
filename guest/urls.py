"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from sign.views import *

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Guest Sign API')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', index),
    url(r'^login_action/$', login_action),
    url(r'^accounts/login/$', index),
    url(r'^event_manage/$', event_manage),
    url(r'^search_name/$', search_name),
    url(r'^guest_manage/$', guest_manage),
    url(r'^sign_index/(?P<eid>[0-9]+)', sign_index),
    url(r'^sign_index_action/(?P<eid>[0-9]+)/$', sign_index_action),
    url(r'^logout/$', logout),

    # url(r'^guest_msg_all/(?P<pid>[0-9]+)/$', GuestViewSet.as_view({'post': 'get_guestmsg'})),
    url(r'^api/', include('sign.urls', namespace="sign")),

    url(r'^$', schema_view)
]

from rest_framework import routers
from sign.views import GuestViewSet

router = routers.DefaultRouter()
router.register(r'api_hzq', GuestViewSet)
urlpatterns += router.urls





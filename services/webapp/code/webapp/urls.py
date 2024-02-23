"""
Webapp URL configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import os
import django
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
import logging

logger = logging.getLogger(__name__)

# Base App
from webapp.core import api as core_api
from webapp.core import views as core_views

# REST Framework & Swagger
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [

    # Views
    url(r'^$', core_views.entrypoint_view),
    path('main/', core_views.main_view),
    path('login/', core_views.login_view),
    path('logout/', core_views.logout_view),
    url(r'^register/$', core_views.register_view),
    url(r'^account/$', core_views.account_view),

    # Admin and API docs (Swagger)
    path('admin/', admin.site.urls),
    path('api/v1/doc/', get_swagger_view(title="Swagger Documentation")),

    # APIs
    path('api/v1/base/login/', core_api.login_api.as_view(), name='login_api'),
    path('api/v1/base/logout/', core_api.logout_api.as_view(), name='logout_api'),

]


#============================
#  Serve static if required
#============================

# Get admin files location
admin_files_path = '/'.join(django.__file__.split('/')[0:-1]) + '/contrib/admin/static/admin'
 
if not settings.DEBUG:

    # Admin files
    urlpatterns.append(url(r'^static/admin/(?P<path>.*)$', django.views.static.serve, {'document_root': admin_files_path} ))

    # Web App core files
    document_root = 'webapp/core/static'
     
    if os.path.isdir(document_root):
        logger.info('Serving static files for app "core" from document root "{}"'.format(document_root))
        # Static
        urlpatterns.append(url(r'^static/(?P<path>.*)$', django.views.static.serve, {'document_root': document_root} ))
    else:
        logger.warning('Not static files to serve?!')
else:
    logger.info('Not serving static files at all as DEBUG=True (Django will do it automatically)')



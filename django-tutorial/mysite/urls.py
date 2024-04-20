"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

# The include() function allows referencing other URLconfs.
# Whenever Django encounters include(), it chops off whatever part of the URL
# matched up to that point and sends the remaining string to the included
# URLconf for further processing.
# You should always use include() when you include other URL patterns.
# admin.site.urls is the only exception to this.
urlpatterns = [
    path("", include("home.urls")),
    path("accounts/", include("accounts.urls")),
    path("orm/", include("orm.urls")),
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
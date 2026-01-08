"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("overview_servers", views.overview_servers, name="overview_servers"),
    path("servers/", views.server_list, name="server_list"),
    path("servers/create/", views.server_create, name="server_create"),
    path("servers/<uuid:pk>/", views.server_detail, name="server_detail"),
    path("servers/<uuid:pk>/update/", views.server_update, name="server_update"),
    path("servers/<uuid:pk>/delete/", views.server_delete, name="server_delete"),
]
"""
URL configuration for h2blueprint project.

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
from user_management.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('ai_process/', include('ai_process.urls')),
    # path('board/', include('board.urls')),
    # path('sensor_data/', include('sensor_data.urls')),
    # path('server_connection/', include('server_connection.urls')),
    # path('status_check/', include('status_check.urls')),
    path('user_management/', include('user_management.urls')),
    path('', home),
]

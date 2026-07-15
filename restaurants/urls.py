"""
URL configuration for mysite project.

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
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.root_redirect, name='root'),
    path('', include('pwa.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    from django.contrib import admin
    urlpatterns.insert(2, path('admin/', admin.site.urls))
urlpatterns += i18n_patterns(
    path('<str:bases>/', views.home_menu, name='home_menu'),
    path('<str:bases>/<str:path>/', views.menu_list, name='menu_list'),
    path('<str:bases>/<str:path>/<str:meal>/', views.menu_detail, name='menu_detail'),
    prefix_default_language=True,
)
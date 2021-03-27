"""Django_starter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token
from django.views.generic import TemplateView
# from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, \
#     password_reset_complete
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static
from core import views

router = SimpleRouter()
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path(r'home/', views.home, name='home'),
                  path(r'page1/', views.page1, name='page1'),
                  # path(r'login/$', auth_views.login, name='login'),
                  path(r'logout/', views.logout_view, name='logout_user'),
                  path(r'get_this_town/(?P<pk>\d+)/$', views.get_this_town, name='get_this_town'),

                  # API URLs
                  path('base-api/', include('rest_framework.urls', namespace='rest_framework')),
                  path('base-api/login_user/', views.LoginView.as_view(), name='login'),
                  path('base-api/hello/', views.HelloView.as_view(), name='hello'),
                  path('base-api/get_towns/', views.TownsView.as_view(), name='get_towns'),

                  path('base-api/logout_user/', views.LogoutView.as_view(), name='logout'),
                  path('base-api/get_users/', views.UsersView.as_view(), name='get_users'),
                  path('base-api/get_groups/', views.GroupsView.as_view(), name='get_groups'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

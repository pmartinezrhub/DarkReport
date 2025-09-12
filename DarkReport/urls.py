"""
URL configuration for DarkReport project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from . import views
from django.conf.urls.static import static
from django.conf import settings
import os 
from django.conf.urls.i18n import set_language
from django.conf.urls.i18n import i18n_patterns
from django.urls import include

urlpatterns = [
    path('', views.dashboard, name='dashboard'), 
    path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('projects/new/', views.project_create, name='project_create'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/add-report/', views.add_report, name='add_report'),
    path('add-report/', views.add_report, name='add_report'),
    path('report/<int:report_id>/add-find/', views.add_find, name='add_find'),
    path('find/<int:pk>/edit/', views.edit_find, name='edit_find'),
    path('find/<int:pk>/delete/', views.delete_find, name='delete_find'),
    path('report/<int:pk>/delete/', views.delete_report, name='delete_report'),
    path('project/<int:pk>/delete/', views.delete_project, name='delete_project'),
    path("cve-lookup/", views.cve_lookup, name="cve_lookup"),
    path('graph-data/', views.graph_data, name='graph_data'),
    path('export_report/<int:report_id>/', views.export_report, name='export_report'),
    path('project/<int:project_id>/export/', views.export_project, name='export_project'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('i18n/', include('django.conf.urls.i18n')),

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


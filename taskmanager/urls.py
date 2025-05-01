"""
URL configuration for taskmanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from tasks import api as tasks_api
from tasks.views import http_debug

urlpatterns = [
    # Use custom admin URLs to ensure proper loading
    path('admin/', include('tasks.admin_urls')),
    path('', include('tasks.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='tasks/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Debug route
    path('http-debug/', http_debug, name='http_debug'),
    
    # API endpoints for WordPress integration
    path('api/tasks/', tasks_api.task_list_api, name='api_tasks_list'),
    path('api/tasks/<int:task_id>/', tasks_api.task_detail_api, name='api_task_detail'),
    path('api/tasks/create/', tasks_api.create_task_api, name='api_create_task'),
    path('api/tasks/<int:task_id>/update-status/', tasks_api.update_task_status_api, name='api_update_task_status'),
    path('api/tasks/<int:task_id>/add-comment/', tasks_api.add_comment_api, name='api_add_comment'),
    
    # Explicit static file serving for development
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# Always include static file patterns regardless of DEBUG setting
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

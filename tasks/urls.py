from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/update/', views.update_task, name='update_task'),
    path('tasks/<int:task_id>/pick/', views.pick_task, name='pick_task'),
    
    # Project URLs
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/update/', views.update_project, name='update_project'),
    
    # Website Sections URLs
    path('projects/<int:project_id>/sections/', views.website_sections, name='website_sections'),
    path('projects/<int:project_id>/sections/add/', views.add_website_section, name='add_website_section'),
    path('website-section/<int:section_id>/edit/', views.edit_website_section, name='edit_website_section'),
    path('website-section/<int:section_id>/delete/', views.delete_website_section, name='delete_website_section'),
    path('api/website-section/<int:section_id>/', views.get_website_section, name='get_website_section'),
    
    # Research Task URLs
    path('research/', views.research_list, name='research_list'),
    path('research/create/', views.create_research_task, name='create_research_task'),
    path('projects/<int:project_id>/research/create/', views.create_research_task, name='create_project_research_task'),
    path('research/<int:research_id>/', views.research_task_detail, name='research_task_detail'),
    path('research/<int:research_id>/update/', views.update_research_task, name='update_research_task'),
    path('research/<int:research_id>/pick/', views.pick_research_task, name='pick_research_task'),
    path('research/<int:research_id>/delete/', views.delete_research_task, name='delete_research_task'),
] 
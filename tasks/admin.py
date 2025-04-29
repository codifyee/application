from django.contrib import admin
from .models import Task, TaskHistory, Comment, Project, ResearchTask

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    list_filter = ('created_by',)
    search_fields = ('name', 'description')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_by', 'assigned_to', 'created_at', 'deadline', 'project')
    list_filter = ('status', 'created_by', 'assigned_to', 'project')
    search_fields = ('title', 'description')

@admin.register(ResearchTask)
class ResearchTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'category', 'created_by', 'assigned_to', 'created_at')
    list_filter = ('project', 'category', 'created_by', 'assigned_to')
    search_fields = ('title', 'description', 'findings')

@admin.register(TaskHistory)
class TaskHistoryAdmin(admin.ModelAdmin):
    list_display = ('task', 'previous_status', 'new_status', 'updated_by', 'updated_at')
    list_filter = ('updated_by',)
    search_fields = ('task__title',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'created_at')
    list_filter = ('user',)
    search_fields = ('content', 'task__title')

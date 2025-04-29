from django import forms
from .models import Task, Comment, Project, ResearchTask, WebsiteSection

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

class WebsiteSectionForm(forms.ModelForm):
    class Meta:
        model = WebsiteSection
        fields = ['page_section', 'subsection', 'content_idea', 'research_notes', 
                 'status', 'assigned_to', 'deadline', 'priority', 'remarks']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'content_idea': forms.Textarea(attrs={'rows': 3}),
            'research_notes': forms.Textarea(attrs={'rows': 3}),
            'remarks': forms.Textarea(attrs={'rows': 2}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'assigned_to', 'deadline', 'project']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']

class ResearchTaskForm(forms.ModelForm):
    class Meta:
        model = ResearchTask
        fields = ['title', 'description', 'assigned_to', 'project', 'status', 'reference_website', 'issues']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'issues': forms.Textarea(attrs={'rows': 3}),
            'reference_website': forms.URLInput(attrs={'placeholder': 'https://example.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].required = True
        self.fields['title'].required = True
        self.fields['description'].required = True

class ResearchFindingsForm(forms.ModelForm):
    class Meta:
        model = ResearchTask
        fields = ['findings']
        widgets = {
            'findings': forms.Textarea(attrs={'rows': 5}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        } 
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task, TaskHistory, Project, ResearchTask, WebsiteSection, Comment
from .forms import TaskForm, TaskStatusForm, CommentForm, ProjectForm, ResearchTaskForm, ResearchFindingsForm, WebsiteSectionForm
import json

@login_required
def task_list(request):
    tasks = Task.objects.all()
    context = {
        'tasks': tasks,
        'todo_count': tasks.filter(status='todo').count(),
        'in_progress_count': tasks.filter(status='in_progress').count(),
        'done_count': tasks.filter(status='done').count(),
        'blocked_count': tasks.filter(status='blocked').count(),
    }
    return render(request, 'tasks/task_list.html', context)

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task_history = task.history.all().order_by('-updated_at')
    comments = task.comments.all().order_by('-created_at')
    comment_form = CommentForm()
    status_form = TaskStatusForm(instance=task)
    
    if request.method == 'POST':
        if 'comment_submit' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.task = task
                comment.user = request.user
                comment.save()
                messages.success(request, 'Comment added successfully.')
                return redirect('task_detail', task_id=task.id)
        
        if 'status_submit' in request.POST:
            status_form = TaskStatusForm(request.POST, instance=task)
            if status_form.is_valid():
                previous_status = task.status
                updated_task = status_form.save()
                
                # Record task history
                TaskHistory.objects.create(
                    task=task,
                    previous_status=previous_status,
                    new_status=updated_task.status,
                    updated_by=request.user
                )
                
                messages.success(request, 'Task status updated successfully.')
                return redirect('task_detail', task_id=task.id)
    
    context = {
        'task': task,
        'task_history': task_history,
        'comments': comments,
        'comment_form': comment_form,
        'status_form': status_form,
    }
    return render(request, 'tasks/task_detail.html', context)

@login_required
def create_task(request):
    project_id = request.GET.get('project')
    project = None
    
    if project_id:
        project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            
            # If project is provided in the URL but not in the form
            if project and not task.project:
                task.project = project
                
            task.save()
            messages.success(request, 'Task created successfully.')
            
            # Redirect to project detail if the task is associated with a project
            if task.project:
                return redirect('project_detail', project_id=task.project.id)
            return redirect('task_list')
    else:
        # Pre-populate project field if provided in URL
        initial_data = {}
        if project:
            initial_data['project'] = project
        form = TaskForm(initial=initial_data)
    
    context = {
        'form': form,
        'is_create': True,
        'project': project,
    }
    return render(request, 'tasks/task_form.html', context)

@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskForm(instance=task)
    
    context = {
        'form': form,
        'is_create': False,
        'task': task,
    }
    return render(request, 'tasks/task_form.html', context)

@login_required
def pick_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if task.assigned_to is not None:
        messages.error(request, 'This task is already assigned.')
    else:
        task.assigned_to = request.user
        task.save()
        messages.success(request, 'You have successfully picked this task.')
    
    return redirect('task_detail', task_id=task.id)

@login_required
def dashboard(request):
    user_tasks = Task.objects.filter(assigned_to=request.user)
    available_tasks = Task.objects.filter(assigned_to=None)
    projects = Project.objects.all()[:5]
    
    context = {
        'user_tasks': user_tasks,
        'available_tasks': available_tasks,
        'projects': projects,
        'todo_count': user_tasks.filter(status='todo').count(),
        'in_progress_count': user_tasks.filter(status='in_progress').count(),
        'done_count': user_tasks.filter(status='done').count(),
        'blocked_count': user_tasks.filter(status='blocked').count(),
    }
    return render(request, 'tasks/dashboard.html', context)

# Project Views
@login_required
def project_list(request):
    projects = Project.objects.all()
    context = {
        'projects': projects,
    }
    return render(request, 'tasks/project_list.html', context)

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.filter(project=project).order_by('status', '-updated_at')
    research_tasks = ResearchTask.objects.filter(project=project).order_by('status', '-updated_at')
    
    # Group research tasks by category
    research_by_category = {}
    for category, label in ResearchTask.CATEGORY_CHOICES:
        category_tasks = research_tasks.filter(category=category)
        if category_tasks.exists():
            research_by_category[label] = category_tasks
    
    context = {
        'project': project,
        'tasks': tasks,
        'research_tasks': research_tasks,
        'research_by_category': research_by_category,
        'task_count': tasks.count(),
        'research_count': research_tasks.count(),
    }
    return render(request, 'tasks/project_detail.html', context)

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            messages.success(request, 'Project created successfully.')
            return redirect('project_list')
    else:
        form = ProjectForm()
    
    context = {
        'form': form,
        'is_create': True,
    }
    return render(request, 'tasks/project_form.html', context)

@login_required
def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully.')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    
    context = {
        'form': form,
        'is_create': False,
        'project': project,
    }
    return render(request, 'tasks/project_form.html', context)

# Research Task Views
@login_required
def create_research_task(request, project_id=None):
    project = None
    if project_id:
        project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        form = ResearchTaskForm(request.POST)
        if form.is_valid():
            try:
                research_task = form.save(commit=False)
                research_task.created_by = request.user
                
                # Always set the project if it's provided in the URL
                if project:
                    research_task.project = project
                
                # Handle section data
                section_data = request.POST.get('section_data')
                print("Raw section data:", section_data)  # Debug print
                print("Section data type:", type(section_data))
                
                try:
                    if section_data and section_data.strip():
                        try:
                            # Use json.loads to parse the string data into a dictionary
                            parsed_data = json.loads(section_data)
                            print("Parsed section data:", parsed_data)
                            print("Parsed data type:", type(parsed_data))
                            print("Number of sections:", len(parsed_data) if isinstance(parsed_data, dict) else 0)
                            
                            # Validate and preserve section data
                            if isinstance(parsed_data, dict):
                                # Count sections before processing
                                original_section_count = len(parsed_data)
                                print(f"Original section count: {original_section_count}")
                                
                                # Ensure all sections have required fields (but don't drop any)
                                for section_id, section in list(parsed_data.items()):
                                    if not isinstance(section, dict):
                                        # Convert non-dict values to proper section format
                                        section = {'name': str(section), 'notes': '', 'references': '', 'status': 'not_started'}
                                        parsed_data[section_id] = section
                                    
                                    # Ensure all required fields exist with defaults
                                    if 'name' not in section or not section['name']:
                                        section['name'] = f"Section {section_id}"
                                    if 'notes' not in section:
                                        section['notes'] = ''
                                    if 'references' not in section:
                                        section['references'] = ''
                                    if 'status' not in section:
                                        section['status'] = 'not_started'
                                
                                # Verify no sections were lost in processing
                                final_section_count = len(parsed_data)
                                if final_section_count != original_section_count:
                                    print(f"WARNING: Section count changed during processing: {original_section_count} -> {final_section_count}")
                                
                                # Save all sections without filtering
                                research_task.section_data = parsed_data
                                print(f"Saving {len(parsed_data)} sections")
                                print("Section keys:", sorted(list(parsed_data.keys())))
                        except json.JSONDecodeError as e:
                            print("JSON decode error:", str(e))  # Debug print
                            research_task.section_data = {
                                'section_1': {
                                    'name': 'Default Section',
                                    'notes': '',
                                    'references': '',
                                    'status': 'not_started'
                                }
                            }
                    else:
                        print("Section data is empty, using default dict")
                        research_task.section_data = {
                            'section_1': {
                                'name': 'Default Section',
                                'notes': '',
                                'references': '',
                                'status': 'not_started'
                            }
                        }
                except Exception as e:
                    print("Unexpected error processing section data:", str(e))
                    research_task.section_data = {
                        'section_1': {
                            'name': 'Default Section',
                            'notes': '',
                            'references': '',
                            'status': 'not_started'
                        }
                    }
                
                research_task.save()
                print("Research task saved with section data:", research_task.section_data)  # Debug print
                print("Section items count:", len(research_task.section_data) if research_task.section_data else 0)
                print("Section keys:", list(research_task.section_data.keys()) if research_task.section_data else [])
                messages.success(request, 'Research task created successfully.')
                
                # Always redirect to project detail if project is provided
                if project:
                    return redirect('project_detail', project_id=project.id)
                return redirect('research_list')
            except Exception as e:
                print("Error saving research task:", str(e))  # Debug print
                messages.error(request, f'Error creating research task: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        initial_data = {}
        if project:
            initial_data['project'] = project
        form = ResearchTaskForm(initial=initial_data)
    
    context = {
        'form': form,
        'is_create': True,
        'project': project,
        'projects': Project.objects.all(),
        'users': User.objects.all(),
    }
    return render(request, 'tasks/research_task_form.html', context)

@login_required
def research_task_detail(request, research_id):
    research_task = get_object_or_404(ResearchTask, id=research_id)
    findings_form = ResearchFindingsForm(instance=research_task)
    
    print("Research task section data:", research_task.section_data)
    print("Section data type:", type(research_task.section_data))
    print("Section items count:", len(research_task.section_data) if research_task.section_data else 0)
    print("Section keys:", list(research_task.section_data.keys()) if research_task.section_data else [])
    
    if request.method == 'POST':
        findings_form = ResearchFindingsForm(request.POST, instance=research_task)
        if findings_form.is_valid():
            findings_form.save()
            messages.success(request, 'Research findings updated successfully.')
            return redirect('research_task_detail', research_id=research_task.id)
    
    context = {
        'research_task': research_task,
        'findings_form': findings_form,
    }
    return render(request, 'tasks/research_task_detail.html', context)

@login_required
def update_research_task(request, research_id):
    research_task = get_object_or_404(ResearchTask, id=research_id)
    
    if request.method == 'POST':
        # Debug: Print all POST data
        print("POST data:", request.POST)
        
        form = ResearchTaskForm(request.POST, instance=research_task)
        if form.is_valid():
            try:
                research_task = form.save(commit=False)
                
                # Handle section data
                section_data = request.POST.get('section_data')
                print("Raw section data:", section_data)  # Debug print
                print("Section data type:", type(section_data))  # Debug print
                
                try:
                    if section_data and section_data.strip():
                        try:
                            # Use json.loads to parse the string data into a dictionary
                            parsed_data = json.loads(section_data)
                            print("Parsed section data:", parsed_data)
                            print("Parsed data type:", type(parsed_data))
                            print("Number of sections:", len(parsed_data) if isinstance(parsed_data, dict) else 0)
                            
                            # Validate and preserve section data
                            if isinstance(parsed_data, dict):
                                # Count sections before processing
                                original_section_count = len(parsed_data)
                                print(f"Original section count: {original_section_count}")
                                
                                # Ensure all sections have required fields (but don't drop any)
                                for section_id, section in list(parsed_data.items()):
                                    if not isinstance(section, dict):
                                        # Convert non-dict values to proper section format
                                        section = {'name': str(section), 'notes': '', 'references': '', 'status': 'not_started'}
                                        parsed_data[section_id] = section
                                    
                                    # Ensure all required fields exist with defaults
                                    if 'name' not in section or not section['name']:
                                        section['name'] = f"Section {section_id}"
                                    if 'notes' not in section:
                                        section['notes'] = ''
                                    if 'references' not in section:
                                        section['references'] = ''
                                    if 'status' not in section:
                                        section['status'] = 'not_started'
                                
                                # Verify no sections were lost in processing
                                final_section_count = len(parsed_data)
                                if final_section_count != original_section_count:
                                    print(f"WARNING: Section count changed during processing: {original_section_count} -> {final_section_count}")
                                
                                # Save all sections without filtering
                                research_task.section_data = parsed_data
                                print(f"Saving {len(parsed_data)} sections")
                                print("Section keys:", sorted(list(parsed_data.keys())))
                        except json.JSONDecodeError as e:
                            print("JSON decode error:", str(e))  # Debug print
                            research_task.section_data = {
                                'section_1': {
                                    'name': 'Default Section',
                                    'notes': '',
                                    'references': '',
                                    'status': 'not_started'
                                }
                            }
                    else:
                        print("Section data is empty, using default dict")
                        research_task.section_data = {
                            'section_1': {
                                'name': 'Default Section',
                                'notes': '',
                                'references': '',
                                'status': 'not_started'
                            }
                        }
                except Exception as e:
                    print("Unexpected error processing section data:", str(e))
                    research_task.section_data = {
                        'section_1': {
                            'name': 'Default Section',
                            'notes': '',
                            'references': '',
                            'status': 'not_started'
                        }
                    }
                
                research_task.save()
                print("Research task saved with section data:", research_task.section_data)  # Debug print
                print("Section items count:", len(research_task.section_data) if research_task.section_data else 0)
                print("Section keys:", list(research_task.section_data.keys()) if research_task.section_data else [])
                messages.success(request, 'Research task updated successfully.')
                return redirect('research_task_detail', research_id=research_task.id)
            except Exception as e:
                print("Error updating research task:", str(e))  # Debug print
                messages.error(request, f'Error updating research task: {str(e)}')
        else:
            print("Form errors:", form.errors)  # Debug print
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ResearchTaskForm(instance=research_task)
    
    context = {
        'form': form,
        'is_create': False,
        'research_task': research_task,
        'project': research_task.project,
        'projects': Project.objects.all(),
        'users': User.objects.all(),
    }
    return render(request, 'tasks/research_task_form.html', context)

@login_required
def pick_research_task(request, research_id):
    research_task = get_object_or_404(ResearchTask, id=research_id)
    
    if research_task.assigned_to is not None:
        messages.error(request, 'This research task is already assigned.')
    else:
        research_task.assigned_to = request.user
        research_task.save()
        messages.success(request, 'You have successfully picked this research task.')
    
    return redirect('research_task_detail', research_id=research_task.id)

@login_required
def website_sections(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    sections = WebsiteSection.objects.filter(project=project)
    users = User.objects.all()
    
    context = {
        'project': project,
        'sections': sections,
        'users': users,
    }
    return render(request, 'tasks/website_sections.html', context)

@login_required
def add_website_section(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        form = WebsiteSectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.project = project
            section.save()
            messages.success(request, 'Website section added successfully.')
            return redirect('website_sections', project_id=project.id)
    else:
        form = WebsiteSectionForm()
    
    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'tasks/website_sections.html', context)

@login_required
def edit_website_section(request, section_id):
    section = get_object_or_404(WebsiteSection, id=section_id)
    
    if request.method == 'POST':
        form = WebsiteSectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            messages.success(request, 'Website section updated successfully.')
            return redirect('website_sections', project_id=section.project.id)
    else:
        form = WebsiteSectionForm(instance=section)
    
    context = {
        'form': form,
        'section': section,
        'project': section.project,
    }
    return render(request, 'tasks/website_sections.html', context)

@login_required
def delete_website_section(request, section_id):
    section = get_object_or_404(WebsiteSection, id=section_id)
    project_id = section.project.id
    
    if request.method == 'POST':
        section.delete()
        messages.success(request, 'Website section deleted successfully.')
        return redirect('website_sections', project_id=project_id)
    
    return redirect('website_sections', project_id=project_id)

# API endpoint for getting section data
@login_required
def get_website_section(request, section_id):
    section = get_object_or_404(WebsiteSection, id=section_id)
    data = {
        'id': section.id,
        'page_section': section.page_section,
        'subsection': section.subsection,
        'content_idea': section.content_idea,
        'research_notes': section.research_notes,
        'status': section.status,
        'assigned_to': section.assigned_to.id if section.assigned_to else None,
        'deadline': section.deadline.strftime('%Y-%m-%d') if section.deadline else None,
        'priority': section.priority,
        'remarks': section.remarks,
    }
    return JsonResponse(data)

@login_required
def research_list(request):
    research_tasks = ResearchTask.objects.all().order_by('-created_at')
    projects = Project.objects.all()
    
    # Apply filters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    project_filter = request.GET.get('project', '')
    
    if search_query:
        research_tasks = research_tasks.filter(title__icontains=search_query)
    
    if status_filter:
        research_tasks = research_tasks.filter(status=status_filter)
    
    if project_filter:
        research_tasks = research_tasks.filter(project_id=project_filter)
    
    context = {
        'research_tasks': research_tasks,
        'users': User.objects.all(),
        'projects': projects,
        'active_project_id': project_filter
    }
    return render(request, 'tasks/research_list.html', context)

@login_required
def delete_research_task(request, research_id):
    research_task = get_object_or_404(ResearchTask, id=research_id)
    
    if request.method == 'POST':
        project_id = research_task.project.id
        research_task.delete()
        messages.success(request, 'Research task deleted successfully.')
        return redirect('project_detail', project_id=project_id)
    
    return redirect('research_list')

# Debug view - no login required, explicitly returns HTTP response
def http_debug(request):
    protocol = request.is_secure() and "HTTPS" or "HTTP"
    return HttpResponse(f"Protocol: {protocol}<br>You have successfully reached the server via HTTP.<br>If you're seeing this, your browser is not forcing HTTPS.")

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Task, TaskHistory, Comment
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

def task_list_api(request):
    """
    API endpoint to get a list of tasks.
    This is used by the WordPress frontend to display tasks.
    """
    tasks = Task.objects.all().order_by('-created_at')
    tasks_data = []
    
    for task in tasks:
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'created_by': task.created_by.username,
            'assigned_to': task.assigned_to.username if task.assigned_to else None,
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat(),
            'deadline': task.deadline.isoformat() if task.deadline else None,
        }
        tasks_data.append(task_data)
    
    return JsonResponse(tasks_data, safe=False)

def task_detail_api(request, task_id):
    """
    API endpoint to get details of a specific task.
    """
    try:
        task = Task.objects.get(id=task_id)
        
        # Get task history
        history = []
        for h in task.history.all().order_by('-updated_at'):
            history.append({
                'id': h.id,
                'previous_status': h.previous_status,
                'new_status': h.new_status,
                'updated_by': h.updated_by.username,
                'updated_at': h.updated_at.isoformat(),
            })
        
        # Get comments
        comments = []
        for c in task.comments.all().order_by('-created_at'):
            comments.append({
                'id': c.id,
                'user': c.user.username,
                'content': c.content,
                'created_at': c.created_at.isoformat(),
            })
        
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'created_by': task.created_by.username,
            'assigned_to': task.assigned_to.username if task.assigned_to else None,
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat(),
            'deadline': task.deadline.isoformat() if task.deadline else None,
            'history': history,
            'comments': comments,
        }
        
        return JsonResponse(task_data)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)

@csrf_exempt
@login_required
def create_task_api(request):
    """
    API endpoint to create a new task.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
    try:
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status', 'todo')
        assigned_to_id = request.POST.get('assigned_to')
        deadline = request.POST.get('deadline')
        
        if not title or not description:
            return JsonResponse({'error': 'Title and description are required'}, status=400)
        
        task = Task(
            title=title,
            description=description,
            status=status,
            created_by=request.user,
        )
        
        if assigned_to_id:
            try:
                assigned_to = User.objects.get(id=assigned_to_id)
                task.assigned_to = assigned_to
            except User.DoesNotExist:
                pass
        
        if deadline:
            task.deadline = deadline
        
        task.save()
        
        return JsonResponse({
            'id': task.id,
            'title': task.title,
            'message': 'Task created successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@login_required
def update_task_status_api(request, task_id):
    """
    API endpoint to update a task's status.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
    try:
        task = Task.objects.get(id=task_id)
        new_status = request.POST.get('status')
        
        if not new_status:
            return JsonResponse({'error': 'Status is required'}, status=400)
        
        if new_status not in [s[0] for s in Task.STATUS_CHOICES]:
            return JsonResponse({'error': 'Invalid status'}, status=400)
        
        previous_status = task.status
        task.status = new_status
        task.save()
        
        # Record task history
        TaskHistory.objects.create(
            task=task,
            previous_status=previous_status,
            new_status=new_status,
            updated_by=request.user
        )
        
        return JsonResponse({
            'id': task.id,
            'status': task.status,
            'message': 'Task status updated successfully'
        })
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@login_required
def add_comment_api(request, task_id):
    """
    API endpoint to add a comment to a task.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
    try:
        task = Task.objects.get(id=task_id)
        content = request.POST.get('content')
        
        if not content:
            return JsonResponse({'error': 'Comment content is required'}, status=400)
        
        comment = Comment.objects.create(
            task=task,
            user=request.user,
            content=content
        )
        
        return JsonResponse({
            'id': comment.id,
            'task_id': task.id,
            'user': request.user.username,
            'content': comment.content,
            'created_at': comment.created_at.isoformat(),
            'message': 'Comment added successfully'
        })
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 
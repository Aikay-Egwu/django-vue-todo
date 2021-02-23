import json
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.middleware.csrf import get_token

from .forms import TaskForm

from .models import Task

def generate_csrf(request):
  return JsonResponse({'csrf_token': get_token(request)}, status=200)   


class TaskView(View):
  def get(self, request):
    #check if request is ajax
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
      tasks = list(Task.objects.values())
      return JsonResponse(tasks, safe=False, status=200)
    return render(request, 'task/tasks.html')
    #set safe to false to return list, default is dictionary

  


  def post(self, request):
    task = json.loads(request.body)
    bound_form = TaskForm(task)

    if bound_form.is_valid():
      new_task = bound_form.save()
      return JsonResponse({'task': model_to_dict(new_task)})
    return redirect('task_list_url')


class TaskPost(View):
  def post(self, request):
    task = json.loads(request.body)
    bound_form = TaskForm(task)

    if bound_form.is_valid():
      new_task = bound_form.save()
      return JsonResponse({'task': model_to_dict(new_task)})
    return redirect('task_list_url')
    
      
class TaskDelete(View):
  def delete(self, request):
    response = json.loads(request.body)
    print()
    print(response)
    print()

    task = Task.objects.get(id=response.get('id'))
    task.delete()
    return JsonResponse({'result': 'OK'})


class TaskUpdate(View):
  def put(self, request):
    response = json.loads(request.body)
    task = Task.objects.get(id=response.get('id'))
    task.completed = not response.get("completed")
    task.save()
    return JsonResponse({'task': model_to_dict(task)})
    return JsonResponse({'result': 'OK'})

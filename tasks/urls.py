from django.urls import path
from .views import *

urlpatterns = [
  path('', TaskView.as_view(), name='task_list_url'),
  path('csrf', generate_csrf),
  path('create', TaskPost.as_view(), name='task_post_url'),
  path('delete', TaskDelete.as_view(), name='task_delete_url'),
  path('update', TaskUpdate.as_view(), name='task_update_url'),
]
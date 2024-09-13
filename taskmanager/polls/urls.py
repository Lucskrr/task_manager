from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, task_list, task_create, task_edit, task_delete, dashboard
from .views import user_logout

urlpatterns = [
    path('', task_list, name='task-list'),
    path('login/', auth_views.LoginView.as_view(template_name='tasks/login.html'), name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('create/', task_create, name='task-create'),
    path('edit/<int:pk>/', task_edit, name='task-edit'),
    path('delete/<int:pk>/', task_delete, name='task-delete'),
    path('dashboard/', dashboard, name='dashboard'),
]

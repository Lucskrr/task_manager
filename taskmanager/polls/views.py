from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Task
from .forms import TaskForm
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect


# Função para registrar novos usuários
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Faz o login automaticamente após o registro
            messages.success(request, 'Registro bem-sucedido! Você está logado.')
            return redirect('task-list')  # Redireciona para a lista de tarefas após o registro
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})

# Função para listar as tarefas do usuário logado
@login_required
def task_list(request):
    tasks = Task.objects.filter(assigned_to=request.user)  # Filtra tarefas atribuídas ao usuário logado
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

# Função para criar uma nova tarefa
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_to = request.user  # Atribui a tarefa ao usuário logado
            task.save()
            messages.success(request, 'Tarefa criada com sucesso!')
            return redirect('task-list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

# Função para editar uma tarefa existente
@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)  # Garante que apenas o dono da tarefa pode editá-la
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarefa atualizada com sucesso!')
            return redirect('task-list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

# Função para deletar uma tarefa
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Tarefa deletada com sucesso!')
        return redirect('task-list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

# Função para o dashboard que mostra todas as tarefas
@login_required
def dashboard(request):
    tasks = Task.objects.all()  # Exibe todas as tarefas no sistema
    pending_tasks = tasks.filter(status='pending').count()
    in_progress_tasks = tasks.filter(status='in_progress').count()
    completed_tasks = tasks.filter(status='completed').count()
    return render(request, 'tasks/dashboard.html', {
        'tasks': tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
    })

def user_logout(request):
    logout(request)
    return redirect('login')


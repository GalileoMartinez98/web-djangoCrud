from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .foms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

# vista home

def home(request):
    return render(request, 'home.html')

# para el formulario
def signup(request):

    if request.method == 'GET':
        print('enviando formulario')

        return render(request, 'signup.html', {'form': UserCreationForm})

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:

                # register user
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')

            except IntegrityError:
                return render(request, 'signup.html', {'form': UserCreationForm,
                                                       "error": 'el usuario ya existe'})

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'password do not match'
        })

@login_required
def tasks(request):
    # hacer una consulta
    tasks = Task.objects.filter(user = request.user, datecompleted__isnull = True)
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completed(request):
    # hacer una consulta
    tasks = Task.objects.filter(user = request.user, datecompleted__isnull = False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
# crear tarea
def create_Task(request):

    if request.method == 'GET':
        return render(request, 'create_task.html',{
            'form':TaskForm
    })

    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit = False) #para guardar datos
            new_task.user = request.user    #usuario de la tarea
            new_task.save()     #guardarlos realmente
            return redirect('tasks')   #para direccionar esa pagina
        except ValueError:
             return render(request, 'create_task.html', {
                'form' : TaskForm,
                'error': 'Please provide valid data'
             })

@login_required
#otra funcion para obtener tareas
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user = request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html',{'task': task, 'form' : form })
    else:
        try:
            task = get_object_or_404(Task, pk = task_id, user = request.user)
            form = TaskForm(request.POST, instance = task)
            form.save()
            return redirect('tasks') 

        except ValueError:
            return render(request, 'task_detail.html',{'task': task, 'form' : form, 'error': "Error al actualizar la tarea" })

@login_required
# vista para tareas actualizadas
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id, user = request.user)

    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
#borrar tarea
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id, user = request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
# funcion para salir o cerrar sesion
def signout(request):
    logout(request)
    return redirect('home')


# funcion para las cuentas ya creadas
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        print(request.POST)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'username or passwor is incorrect'
            })

        else:
            login(request, user)
            return redirect('tasks')


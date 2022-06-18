# todo/views
from django.shortcuts import render, redirect, get_object_or_404
# Импортируем форму для регистрации и авторизации
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Импортируем модель пользователя
from django.contrib.auth.models import User
# Импортируем ошибку
from django.db import IntegrityError
# Импортируем логин и логаут
from django.contrib.auth import login, logout, authenticate
# Импортируем кастомную форму
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Функция для прогрузки домашней страницы
def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):

    # Если мы создаем нового пользователя.
    # Если мы вводим адрес в браузере, то мы всегда используем метод GET
    # POST работает только при вводе данных через различные формы
    if request.method == 'GET':
        return render(
            request,
            'todo/signupuser.html',
            {'form': UserCreationForm()})

    else:
        # Проверяем соответствия пароля 1 и 2
        if request.POST['password1'] == request.POST['password2']:

            # Возможно создать нового пользователя только в
            # случае соответствия пароля 1 и пароля 2
            # Вся информация о новом пользователе вносится в базу
            # данных автоматически
            # Create_user - встроенная функция в джанго,
            # которая позволяет создавать новых пользователей
            # В скобках передаются данные. Возвращается по ключу в словаре.
            # Какой конкретно ключ надо передавать
            # можно посмотреть в инспекторе кода
            try:
                # Пытаемся сохранить пользователя
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')

            except IntegrityError:
                # Если не получается, то адресуем пользователя
                # на другую страницу с соответствующим сообщением
                return render(
                    request, 'todo/signupuser.html',
                    {'form': UserCreationForm(),
                     'error':
                     'This username has already been taken. '
                     'Please choose a new one'}
                )
        else:

            # Сообщаем пользователю о несоответствии паролей
            return render(
                request, 'todo/signupuser.html',
                {'form': UserCreationForm(),
                 'error': 'passwords did not match'}
            )


def loginuser(request):

    # Мы логиним пользователя
    # Если мы вводим адрес в браузере, то мы всегда используем метод GET
    # POST работает только при вводе данных через различные формы
    if request.method == 'GET':
        return render(
                    request,
                    'todo/loginuser.html',
                    {'form': AuthenticationForm()}
                    )
# Если пользователь ввел верный логин и пароль
    else:
        user = authenticate(
                    request,
                    username=request.POST['username'],
                    password=request.POST['password']
                    )
# Если такого пользователя нет, то мы выводим ошибку и переадресуем его на
# страницу аутентификации повторно
        if user is None:
            return render(
                    request,
                    'todo/loginuser.html',
                    {'form': AuthenticationForm(),
                     'error':
                         'Username and password did not match'}
                    )
# Иначе мы переадресуем его на страницу
# с его заданиями, которые он должен делать
        else:
            login(request, user)
            return redirect('currenttodos')


# Создаем функцию для выхода пользователя. Пользователь
# выходит только после проверки метода обращения. После выхода
# мы перенаправляем его на домашнюю страницу
@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    # Если пользователь внес какую-то информацию и
    # направил запрос на ее размещение:
    else:
        try:
            # Соединяем информацию, полученную формой
            form = TodoForm(request.POST)
            # Сохраняем данные в базу данных
            newtodo = form.save(commit=False)
            # Привязываем запись к конкретному пользователю
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(
                request,
                'todo/createtodo.html',
                {'form': TodoForm(), 'error':
                    'Bad data passed in. Try again.'})


@login_required
def currenttodos(request):
    # делаем фильтр, чтобы пользователь видел только свои записи
    # через фильтр и записываем ее в переменную
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    # передаем все записи
    return render(request,
                  'todo/currenttodos.html',
                  {'todos': todos})


@login_required
def completedtodos(request):
    # делаем фильтр, чтобы пользователь видел только свои записи
    # через фильтр и записываем ее в переменную
    todos = Todo.objects.filter(
        user=request.user,
        datecompleted__isnull=False).order_by(
        '-datecompleted'
    )
    # передаем все записи
    return render(request, 'todo/completedtodos.html', {'todos': todos})


@login_required
def viewtodo(request, todo_pk):
    # изучить эту функцию детально. Судя по всему она возвращает 404 или объект
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        # Уточнение говорит джанго о том,
        # что мы не пытаемся создать новую форму,
        # а изменяем существующий объект
        form = TodoForm(instance=todo)
        # Передаем запись, форму
        return render(
            request, 'todo/viewtodo.html',
            {'todo': todo, 'form': form})
    else:
        try:
            # Уточнение говорит джанго о том, что мы не
            # пытаемся создать новую форму, а изменяем существующий объект
            # Соединяем информацию, полученную формой
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(
                request,
                'todo/viewtodo.html',
                {'todo': todo, 'form': form, 'error': 'Bad info'})


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        # Через datecompleted узнаем выполнена задача или нет.
        # Присвоим текущее значение даты и времени из
        # типа timezone. Данный код будет выполнять текущей датой и
        # временем, в случае выполнения задачи
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

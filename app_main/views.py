
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from app_main.models import Todo
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
# Create your views here.

@login_required(login_url='login/')
def home_page(request):
    todos = Todo.objects.filter(owner=request.user).order_by("-id")

    return render(
        request=request,
        template_name='home_page.html',
        context={ 'todos': todos }
    )

def new_todo_page(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        new_todo = Todo.objects.create(
            owner=request.user,
            title=title,
            description=description,
        )

        if image:
            new_todo.image = image
            new_todo.save()

        return redirect('/')

    return render(request, "new_todo.html")

def todo_edit(request, todo_id):
    todo = Todo.objects.get(id=todo_id)

    if todo.owner != request.user:
        return redirect("/")

    if request.method == 'POST':
        title = request.POST.get("title")
        description = request.POST.get("description")

        todo.title = title
        todo.description = description
        todo.save()
        return redirect('/')
    
    return render(request, 'todo_edit.html', context={"todo": todo})

def todo_delete(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    
    if todo.owner != request.user:
        return redirect("/")

    todo.delete()
    return redirect('/')

def todo_detail(request, todo_id):
    todo = Todo.objects.get(id=todo_id)

    if request.user != todo.owner:
        return redirect("/")

    return render(request, 'todo_detail.html', context={'todo': todo})

def registration_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        user_exists = User.objects.filter(username=username).exists()

        error_messages = []
        
        if user_exists:
            error_messages.append("Bunday 'username' ga ega foydalanuvchi allaqachon mavjud.")

        if not username or not password1 or not password2:
            error_messages.append("'username', 'Parol' va 'Parolni tasdiqlash' majburiy.")

        if password1 != password2:
            error_messages.append("Parollar bir-biriga mos emas.")

        if password2.isdigit():
            error_messages.append("Parol tarkibida harflar ham bo'lishi kerak.")

        if password2.isalpha():
            error_messages.append("Parol tarkibida raqamlar ham bo'lishi kerak.")

        if len(password2) < 8:
            error_messages.append("Parol uzunligi 8 tadan ko'p bo'lishi shart.")

        if len(error_messages) > 0:
            return render(request, "registration_page.html", context={"error_messages": error_messages})

        if not user_exists and  username and password1 and password2 and password1 == password2:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
            )
            user.set_password(raw_password=password2)
            user.save()
            return redirect("/login")

    return render(request, "registration_page.html")

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            user = None

        password_is_valid = False
        if user:
            password_is_valid = user.check_password(raw_password=password)

        if user and password_is_valid:
            login(
                request=request,
                user=user,
            )
            return redirect('/')


    return render(
        request=request,
        template_name='login_page.html',
    )

def logout_page(request):
    logout(request)
    return redirect('/login/')


def send_email(request):
    if request.method == "POST":
        recipient = request.POST.get("recipient")
        subject = request.POST.get("subject")
        body = request.POST.get("body")

        send_mail(
            subject=subject,
            message=body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient],
            fail_silently=False,
        )
        return HttpResponse("<h1>Yuborildi</h1>")

    return render(request, 'send_email.html')
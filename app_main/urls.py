from django.urls import path
from app_main import views

urlpatterns = [
    path('', views.home_page),              # http://127.0.0.1:8000/
    path('registration/', views.registration_page),       # http://127.0.0.1:8000/login/
    path('login/', views.login_page),       # http://127.0.0.1:8000/login/
    path('logout/', views.logout_page),     # http://127.0.0.1:8000/login/
    path('new-todo/', views.new_todo_page),
    path('delete-todo/<int:todo_id>/', views.todo_delete),
    path('edit-todo/<int:todo_id>/', views.todo_edit),
    path('todo-detail/<int:todo_id>/', views.todo_detail),
    path('send-email/', views.send_email),
]
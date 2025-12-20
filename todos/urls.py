# todos/urls.py
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import (
    CustomLoginView,
    RegisterView,
    TaskList,
    TaskCreate,
    TaskUpdate,
    TaskDelete,
    force_login
)

urlpatterns = [
    # روت سایت → همیشه لاگین
    path('', force_login, name='home'),

    # Auth
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    # Tasks
    path('tasks/', TaskList.as_view(), name='task-list'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
]

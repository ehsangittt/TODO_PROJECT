# todos/views.py
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Task


# =========================
# Register
# =========================

class RegisterView(View):
    def get(self, request):
        return render(request, 'todos/register.html', {'form': UserCreationForm()})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task-list')
        return render(request, 'todos/register.html', {'form': form})


# =========================
# Login (همیشه اجازه نمایش بده)
# =========================

class CustomLoginView(LoginView):
    template_name = 'todos/login.html'
    redirect_authenticated_user = False  

    def get_success_url(self):
        return reverse_lazy('task-list')


# =========================
# Force Login (Logout → Login)
# =========================

def force_login(request):
   
    logout(request)
    return redirect('login')


# =========================
# Task List
# =========================

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'todos/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_superuser:
            qs = Task.objects.all()
        else:
            qs = Task.objects.filter(user=self.request.user)

        self.search_input = self.request.GET.get('search-area', '')
        if self.search_input:
            qs = qs.filter(title__icontains=self.search_input)

        self.sort_by = self.request.GET.get('sort', '-created_at')
        return qs.order_by(self.sort_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = self.get_queryset().filter(status='TODO').count()
        context['search_input'] = self.search_input
        context['sort_by'] = self.sort_by
        return context


# =========================
# Create / Update / Delete
# =========================

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'status', 'priority', 'due_date', 'image']
    template_name = 'todos/task_form.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'status', 'priority', 'due_date', 'image']
    template_name = 'todos/task_form.html'
    success_url = reverse_lazy('task-list')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(user=self.request.user)


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'todos/task_confirm_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('task-list')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(user=self.request.user)

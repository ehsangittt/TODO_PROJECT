from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Task

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

class CustomLoginView(LoginView):
    template_name = 'todos/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    def get_success_url(self): return reverse_lazy('task-list')

#class TaskList(LoginRequiredMixin, ListView):
 #   model = Task
  #  context_object_name = 'tasks'
   # template_name = 'todos/task_list.html'
    #def get_queryset(self):
     #   qs = Task.objects.filter(user=self.request.user)
      ## if search: qs = qs.filter(title__icontains=search)
        #return qs
    #def get_context_data(self, **kwargs):
     #   ctx = super().get_context_data(**kwargs)
      #  ctx['count'] = ctx['tasks'].filter(status='TODO').count()
       # return ctx
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'todos/task_list.html'
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Task.objects.all()

        qs = Task.objects.filter(user=self.request.user)
        search = self.request.GET.get('search-area') or ''
        if search: qs = qs.filter(title__icontains=search)
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['count'] = ctx['tasks'].filter(status='TODO').count()
        return ctx

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'status', 'priority', 'due_date']
    success_url = reverse_lazy('task-list')
    template_name = 'todos/task_form.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'status', 'priority', 'due_date']
    success_url = reverse_lazy('task-list')
    template_name = 'todos/task_form.html'
    def get_queryset(self): 
        return self.model.objects.filter(user=self.request.user)

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('task-list')
    template_name = 'todos/task_confirm_delete.html'
    def get_queryset(self): return Task.objects.filter(user=self.request.user)
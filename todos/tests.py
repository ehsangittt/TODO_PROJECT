from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Task

class TaskAppTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task'
        )

    def test_login_required_for_task_list(self):
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 302)  # redirect to login

    def test_user_can_see_own_tasks(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('task-list'))
        self.assertContains(response, 'Test Task')

    def test_api_task_list(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, 200)
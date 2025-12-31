from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.forms import modelform_factory
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from todos.models import Task, Attachment
from todos.serializers import TaskSerializer

# ----------------------------
# Models
# ----------------------------
class TaskAndAttachmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('u1', password='1234')

    def test_task_creation_and_str(self):
        task = Task.objects.create(user=self.user, title='Task1')
        self.assertEqual(str(task), 'Task1')
        self.assertEqual(task.status, 'TODO')

    def test_task_validation_failure(self):
        task = Task(user=self.user, title='')
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_attachment_creation(self):
        task = Task.objects.create(user=self.user, title='Task2')
        file = SimpleUploadedFile("file.txt", b"content")
        attachment = Attachment.objects.create(task=task, file=file)
        self.assertEqual(str(attachment), f"Attachment for {task.title}")

# ----------------------------
# Forms
# ----------------------------
TaskForm = modelform_factory(Task, fields=['title','description','status','priority'])

class TaskFormTest(TestCase):
    def test_form_valid_and_invalid(self):
        valid_form = TaskForm(data={'title':'T','status':'TODO','priority':'MEDIUM'})
        self.assertTrue(valid_form.is_valid())
        invalid_form = TaskForm(data={'title':'','status':'TODO'})
        self.assertFalse(invalid_form.is_valid())

# ----------------------------
# Views
# ----------------------------
class TaskViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('u1', password='1234')
        self.other = User.objects.create_user('u2', password='1234')
        Task.objects.create(user=self.user, title='MyTask')
        Task.objects.create(user=self.other, title='OtherTask')

    def test_list_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 302)

    def test_list_view_user_tasks_only(self):
        self.client.login(username='u1', password='1234')
        resp = self.client.get(reverse('task-list'))
        tasks = resp.context['tasks']
        self.assertEqual(tasks.count(),1)
        self.assertEqual(tasks.first().title,'MyTask')

    def test_create_view_success_and_failure(self):
        self.client.login(username='u1', password='1234')
        # success
        resp = self.client.post(reverse('task-create'), {'title':'New','status':'TODO','priority':'MEDIUM'})
        self.assertEqual(Task.objects.filter(user=self.user).count(),2)
        self.assertRedirects(resp, reverse('task-list'))
        # failure
        resp2 = self.client.post(reverse('task-create'), {'title':'','status':'TODO'})
        self.assertEqual(Task.objects.filter(user=self.user).count(),2)
        self.assertEqual(resp2.status_code,200)

# ----------------------------
# Serializers
# ----------------------------
class TaskSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('ser', password='1234')
        self.task = Task.objects.create(user=self.user, title='SerTask', status='DONE')

    def test_serializer_fields_and_read_only_user(self):
        serializer = TaskSerializer(instance=self.task)
        data = serializer.data
        self.assertEqual(data['title'],'SerTask')
        self.assertEqual(data['status'],'DONE')
        self.assertEqual(data['user'],'ser')
        self.assertIn('attachments',data)

        # read-only user
        serializer2 = TaskSerializer(instance=self.task, data={'user':'hacker'}, partial=True)
        serializer2.is_valid()
        self.assertEqual(serializer2.validated_data,{})

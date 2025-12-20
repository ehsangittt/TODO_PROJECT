# todos/serializers.py
from rest_framework import serializers
from .models import Task, Attachment
from django.contrib.auth.models import User

# =========================
# Attachment Serializer
# =========================
class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'file', 'uploaded_at']


# =========================
# Task Serializer
# =========================
class TaskSerializer(serializers.ModelSerializer):
    # شامل تمام attachments مربوط به این Task
    attachments = AttachmentSerializer(many=True, read_only=True)
    
    # نمایش username کاربر به جای id
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'due_date',
            'created_at',
            'attachments',
            'user'
        ]
        read_only_fields = ['user', 'created_at']

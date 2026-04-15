import uuid
from django.db import models
from django.contrib.auth import get_user_model
from blog.models import Blog


User = get_user_model()

class TaskStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PROCESSING = "processing", "Processing"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"


class BlogConversionTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(choices=TaskStatus.choices, default=TaskStatus.PENDING)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    # Using TextField for unpredictable AI response lengths
    prompt = models.TextField() 
    result = models.TextField(null=True, blank=True)
    error_log = models.TextField(null=True, blank=True) # To debug why an AI call failed

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["user_id"]),
            models.Index(fields=["blog_id"]),
        ]


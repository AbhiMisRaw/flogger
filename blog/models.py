from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from utils import Util

User = get_user_model()

class BlogStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"
    ARCHIVED = "archived", "Archived"

class Tag(models.Model):
    """Model for tags."""
    name = models.CharField(
        max_length=50,
        unique=True,
        null=False
    )
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or len(self.slug) == 0:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Blog(models.Model):
    """Model for Blpg model."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="blogs",
        blank=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blogs"
    )
    status = models.CharField(
        choices=BlogStatus.choices,
        default=BlogStatus.DRAFT,
        max_length=25
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug or len(self.slug) == 0:
            self.slug = f"{slugify(self.title)}-{Util.random_code()}"
            print(self.slug)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}. {self.title}"
    
    class Meta:
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["title"]),
            models.Index(fields=["author", "-created_at"]),
        ]
        ordering = ("-created_at",)
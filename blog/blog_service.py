import json
from typing import List
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q

from .forms import BlogForm
from .models import Blog, BlogStatus, Tag

User = get_user_model()


class BlogCoreService:
    """
    Pure business logic.
    Can be reused by MVT views, DRF APIs, Celery, CLI, tests.
    """

    @staticmethod
    def create_blog(
        author,
        title: str,
        content: str,
        status: str,
        tags: list[str] | None = None,
    ) -> Blog:
        status = (
            BlogStatus.DRAFT.value
            if status == "draft"
            else BlogStatus.PUBLISHED.value
        )
        print(tags)
        with transaction.atomic():
            blog = Blog.objects.create(
                title=title,
                content=content,
                status=status,
                author=author,
            )

            if tags:
                tag_objs = [
                    Tag.objects.get_or_create(name=tag.strip())[0]
                    for tag in tags
                ]
                blog.tags.add(*tag_objs)

        return blog

class BlogQueryService:

    @staticmethod
    def get_blog_by_slug(slug: str) -> Blog | None:
        return (
            Blog.objects
            .filter(slug=slug)
            .select_related("author")
            .prefetch_related("tags")
            .first()
        )

    @staticmethod
    def fetch_blogs(*, user_id=None, status=None):
        status = status or BlogStatus.PUBLISHED.value

        qs = Blog.objects.filter(status=status)

        if user_id:
            qs = qs.filter(author_id=user_id)

        return (
            qs.select_related("author")
              .prefetch_related("tags")
              .order_by("-created_at")
        )


class BlogServiceV1:

    @staticmethod
    def validate_form(data, form_class):
        form = form_class(data)
        return form, form.is_valid()

    @staticmethod
    def get_blog(request, slug):
        blog = BlogQueryService.get_blog_by_slug(slug)
        return render(
            request,
            "blogs/homepage.html",
            {
                "blog":blog,
                "tab":"blog_page",
            }
        )

    @staticmethod
    def get_creation_form(request, blog: Blog = None):
        if blog:
            form = BlogForm(blog)
        else:
            form = BlogForm()
        
        context = {
            "title":"Create",
            "form":form,
            "tab":"create"
        }
        return render(request, "blogs/blog-editor.html", context)

    @staticmethod
    def create_blog(request):
        form, is_valid = BlogServiceV1.validate_form(
            request.POST, BlogForm
        )

        if not is_valid:
            return render(
                request,
                "blogs/blog-editor.html",
                {"form": form, "tab": "create"},
            )

        data = form.cleaned_data
        action = request.POST.get("action")
        tags = request.POST.get("tags", "").split(",")

        if action == "publish" and not (3 <= len(tags) <= 5):
            messages.error(request, "Tags must be between 3 and 5.")
            return redirect("blog:create")

        blog = BlogCoreService.create_blog(
            title=data["title"],
            content=data["content"],
            author=request.user,
            status=action,
            tags=tags,
        )

        messages.success(
            request,
            "Draft saved successfully."
            if action == "draft"
            else "Blog published successfully.",
        )
        return redirect("/flog/homepage")

    @staticmethod
    def get_homepage(request):
        query = request.GET.get("search","")
        if query:
            # filtering the blogs
            results = Blog.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ).filter(
                status=BlogStatus.PUBLISHED.value
            )
            return render(
                request,
                "blogs/partial/blogs.html",
                {
                    "blogs":results,
                    "query":query,
                    "tab":"homepage",
                }
            )
        
        blogs = BlogQueryService.fetch_blogs(
            user_id=request.GET.get("user"),
            status=request.GET.get("status"),
        )
        context = {
            "homepage":"active",
            "blogs":blogs,
            "tab":"homepage",
        }
        return render(
            request,
            "blogs/homepage.html",
            context=context
        )

    def update_blog(self, request, blog_id):
        pass


class BlogAPIService(BlogCoreService):

    @staticmethod
    def get_blogs(request):
        
        blogs = BlogQueryService.fetch_blogs(
            user_id=request.GET.get("user"),
            status=request.GET.get("status"),
        )
        data_list = [blog.to_dict() for blog in blogs]
        return JsonResponse(data_list, safe=False, status=200)

    @classmethod
    def handle_blog_creation(cls, request):
        body = json.loads(request.body)
        
        user = User.objects.get(pk=1)
        body["status"] = body.get("status") or "draft"
        blog = BlogCoreService.create_blog(user, **body)
        return JsonResponse(blog.to_dict())

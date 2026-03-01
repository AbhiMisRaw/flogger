import json
from django.http import JsonResponse, HttpResponseForbidden, Http404
from django.core.paginator import Paginator
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
        if blog:
            return render(
                request,
                "blogs/blog.html",
                {
                    "blog":blog,
                    "tab":"blog_page",
                }
            )
        else:
            raise Http404("Page not found")

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
        form, is_valid = BlogServiceV1.validate_form(request.POST, BlogForm)

        if not is_valid:
            return render(
                request,
                "blogs/blog-editor.html",
                {"form": form, "tab": "create"},
            )

        data = form.cleaned_data
        action = request.POST.get("action")
        
        # Safely handle tags (removing empty spaces)
        raw_tags = request.POST.get("tags", "")
        tags = [t.strip() for t in raw_tags.split(",") if t.strip()]

        # Validate tags ONLY if publishing
        if action == "publish" and not (3 <= len(tags) <= 5):
            messages.error(request, "Please provide between 3 and 5 tags to publish.")
            # CRITICAL FIX: Render the form again so the user doesn't lose their writing!
            return render(
                request,
                "blogs/blog-editor.html",
                {"form": form, "tab": "create"},
            )

        blog = BlogCoreService.create_blog(
            title=data["title"],
            content=data["content"],
            author=request.user,
            status=action,
            tags=tags,
        )

        if action == "draft":
            messages.success(request, "Draft saved successfully.")
        else:
            messages.success(request, "Blog published successfully!")
            
        return redirect("blog:home_page")


    @staticmethod
    def get_blogs(page_number=1, blog_obj=10, query=None, tag_slug=None, status=None, user=None):
        # 1. Start with the most restrictive base (always order)
        blogs_queryset = Blog.objects.all().order_by('-created_at')

        # 2. Chain filters (Don't overwrite, just append .filter)
        if status:
            blogs_queryset = blogs_queryset.filter(status=status)
        
        if user:
            blogs_queryset = blogs_queryset.filter(author=user)

        if query:
            blogs_queryset = blogs_queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )

        if tag_slug:
            blogs_queryset = blogs_queryset.filter(tags__slug=tag_slug)

        # 3. Paginate the final result
        paginator = Paginator(blogs_queryset, blog_obj)
        return paginator.get_page(page_number)

    @staticmethod
    def get_homepage(request):
        query = request.GET.get("search", "")
        tag_slug = request.GET.get("tag", "")
        page_number = request.GET.get("page", 1)
        
        # Use your existing get_blogs logic here
        page_obj = BlogServiceV1.get_blogs(
            page_number=page_number,
            query=query,
            tag_slug=tag_slug,
            status=BlogStatus.PUBLISHED.value
        )

        context = {
            "blogs": page_obj,
            "query": query,
            "selected_tag": tag_slug,
        }

        # If HTMX is requesting, just send the partial
        if request.htmx:
            return render(request, "blogs/partial/blogs.html", context)

        # Otherwise, send the full page
        return render(request, "blogs/homepage.html", context)


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
        if not request.user.is_authenticated:
            raise HttpResponseForbidden(content="Please login first")
        
        body = json.loads(request.body)
        user = request.user
        body["status"] = body.get("status") or "draft"
        blog = BlogCoreService.create_blog(user, **body)
        return JsonResponse(blog.to_dict())

import json
from django.http import JsonResponse, HttpResponseForbidden, Http404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator, AsyncPaginator

from django.shortcuts import redirect, render
from django.db import transaction
from django.db.models import Q

from .forms import BlogForm
from .models import Blog, BlogStatus, Tag


User = get_user_model()

class BlogCoreService:
    """Write Only"""
    @staticmethod
    def create_blog(author, title, content, status, tags=None):
        # Map string "publish" from UI to DB Integer/Enum
        status = BlogStatus.PUBLISHED.value if status == "publish" else BlogStatus.DRAFT.value
        
        with transaction.atomic():
            blog = Blog.objects.create(
                title=title, content=content, status=status, author=author
            )
            if tags:
                tag_objs = [Tag.objects.get_or_create(name=t.strip())[0] for t in tags]
                blog.tags.add(*tag_objs)
        return blog

    @staticmethod
    def update_blog(blog_id, actor, **data):
        # Permission logic belongs here
        blog = Blog.objects.get(id=blog_id)
        if blog.author != actor:
            raise PermissionError("You cannot edit this blog.")
        # ... update logic ...
        # TODO
        pass


class BlogQueryService:
    """Get Only"""

    @staticmethod
    async def fetch_blogs(query=None, tag_slug=None, status=None, user=None, page=1, page_size=10):
        # Start with an optimized queryset
        qs = Blog.objects.select_related("author").prefetch_related("tags").order_by('-created_at')

        if status:
            qs = qs.filter(status=status)
        if user:
            qs = qs.filter(author=user)
        if query:
            qs = qs.filter(Q(title__icontains=query) | Q(content__icontains=query))
        if tag_slug:
            # .distinct() is crucial when filtering by M2M tags to avoid duplicates
            qs = qs.filter(tags__slug=tag_slug).distinct()

        paginator = AsyncPaginator(qs, page_size)
        return await paginator.aget_page(page)

    @staticmethod
    def get_by_slug(slug):
        return Blog.objects.filter(slug=slug).filter(status=BlogStatus.PUBLISHED).afirst()


class BlogServiceV1:

    @staticmethod
    def validate_form(data, form_class):
        form = form_class(data)
        return form, form.is_valid()

    @staticmethod
    async def get_blog(request, slug):
        blog = await BlogQueryService.get_by_slug(slug)
        user = await request.auser()
        if blog:
            return render(
                request,
                "blogs/blog.html",
                {
                    "blog":blog,
                    "tab":"blog_page",
                    "user":user,
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
        form = BlogForm(request.POST)
        if not form.is_valid():
            return render(request, "blogs/blog-editor.html", {"form": form, "tab": "create"})

        action = request.POST.get("action")
        tags = [t.strip() for t in request.POST.get("tags", "").split(",") if t.strip()]

        try:
            BlogCoreService.create_blog(
                author=request.user,
                title=form.cleaned_data["title"],
                content=form.cleaned_data["content"],
                status=action,
                tags=tags
            )
            messages.success(request, f"Successfully {action}ed!")
            return redirect("blog:home_page")
        except ValueError as e:
            messages.error(request, str(e))
            return render(request, "blogs/blog-editor.html", {"form": form, "tab": "create"})


    @staticmethod
    async def get_homepage(request):
        query = request.GET.get("search", "")
        tag_slug = request.GET.get("tag", "")
        page_number = request.GET.get("page", 1)
        user = await request.auser()
        print("User : ", user)
        page_obj = await BlogQueryService.fetch_blogs(
            page=page_number,
            query=query,
            tag_slug=tag_slug,
            status=BlogStatus.PUBLISHED.value
        )
        # 2. CRITICAL FIX: Manually await the object list realization
        # This pre-fetches the results so the template doesn't have to 'await'
        await page_obj.aget_object_list()

        context = {
            "blogs": page_obj,
            "query": query,
            "selected_tag": tag_slug,
            "user":user if user is not AnonymousUser else None
            }
        
        template = "blogs/partial/blogs.html" if request.htmx else "blogs/homepage.html"
        return render(request, template, context)


    def update_blog(self, request, blog_id):
        pass


class BlogAPIService(BlogCoreService):

    @staticmethod
    async def get_blogs(request):
        
        blogs = await BlogQueryService.fetch_blogs(
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

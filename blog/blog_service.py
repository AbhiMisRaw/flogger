from django.shortcuts import redirect, render
from django.forms import Form
from django.contrib import messages
from django.db import transaction
from django.db.models import Q

from .forms import BlogForm, TagsForm
from .models import Blog, BlogStatus, Tag

class BlogServiceV1():

    @staticmethod
    def validate_form(data: dict, form_class: Form):
        form = form_class(data)
        if form.is_valid():
            return form, True
        
        return form, False

    @staticmethod
    def get_creation_form(request):
        form = BlogForm()
        tags_form = TagsForm()
        context = {
            "title":"Create",
            "form":form,
            "tags_form":tags_form,
            "tab":"create"
        }
        return render(request, "blogs/blog-editor.html", context)

    @staticmethod
    def create_blog(request):
        user = request.user
        # validating blog
        form, is_valid = BlogServiceV1.validate_form(request.POST, BlogForm)

        if not is_valid:
            context = {
                "title":"Create",
                "form":form,
                "tab":"create"
            }
            return render(request, "blogs/blog-editor.html", context)
        
        
        data = form.cleaned_data
        action = request.POST.get("action")
        is_title_exist = Blog.objects.filter(title=data.get("title"), author=user).exists()

        if is_title_exist:
            print("title already exit!!!")
            form.add_error(None, "Change your title, this title is already exist...")
            context = {
                "title":"Create",
                "form":form,
                "tab":"create"
            }
            return render(request, "blogs/blog-editor.html", context)
        
        blog = Blog.objects.create(
            title=data.get("title"),
            content=data.get("content"),
            status = "",
            author=user
        )

        if action == "draft":
            return redirect("/flog/homepage")
        else:
            tags_raw = request.POST.get("tags", "")
            tags = tags_raw.split(",")

            if not (3 <= len(tags) <= 5):
                messages.error(request, "Tags must be between 3 and 5.")
                return redirect("blog:create")
            
            # 3️⃣ Atomic DB operation
            with transaction.atomic():
                blog = Blog.objects.create(
                    title=data["title"],
                    content=data["content"],
                    status="draft" if action == "draft" else "published",
                    author=user,
                )

                # 4️⃣ Create tags if needed + attach
                if action == "publish":
                    tag_objects = []

                    for tag_name in tags:
                        tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
                        tag_objects.append(tag_obj)

                    blog.tags.add(*tag_objects)

            # 5️⃣ Redirect
            if action == "draft":
                messages.success(request, "Draft saved successfully.")
            else:
                messages.success(request, "Blog published successfully.")

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
        
        blogs = (
            Blog.objects\
            .filter(status=BlogStatus.PUBLISHED.value)\
            # FK → JOIN
            .select_related("author")\
            # M2M → separate query
            .prefetch_related("tags")\
            .only('title', 'content', 'author', 'status', 'created_at')\
            .order_by("-created_at")
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
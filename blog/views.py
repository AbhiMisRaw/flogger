from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Blog
from .forms import BlogForm
# Create your views here.

@login_required
def home(request):
    user = request.user
    blogs = (
        Blog.objects\
        .filter(author=user)\
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
        "homepage.html",
        context=context
    )


def saved_blogs(request):
    """this handler serve those blogs saved by user."""
    context = {
        "saved":"active",
        "tab":"saved",
    }
    return render(
        request,
        "saved.html",
        context=context
    )


def my_blogs(request):
    """this handler serve blogs written by user."""
    context = {
        "saved":"active",
    }
    return render(
        request,
        "saved.html",
        context=context
    )


def search_blogs(request):
    query = request.GET.get("search","")

    # filtering the blogs
    results = Blog.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    )
    return render(
        request,
        "partial/blogs.html",
        {
            "blogs":results,
            "query":query,
            "tab":"search",
        }
    )


def create_blog(request):
    """this handler help to create the blog."""
    print(request.method)
    if request.method == "POST":
        
        return render(request, "")
    elif request.method == "GET":
        form = BlogForm()
        context = {
            "title":"Create",
            "form":form,
            "tab":"create"
        }
        return render(request, "blog-editor.html", context)

    
    
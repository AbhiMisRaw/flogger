from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Blog
from .blog_service import BlogServiceV1
# Create your views here.


class BlogHome(View):
    def get(self, request):
        return BlogServiceV1.get_homepage(request)


def saved_blogs(request):
    """this handler serve those blogs saved by user."""
    context = {
        "saved":"active",
        "tab":"saved",
    }
    return render(
        request,
        "blogs/saved.html",
        context=context
    )


def my_blogs(request):
    """This handler serve blogs written by user."""
    
    context = {
        "saved":"active",
    }
    return render(
        request,
        "blogs/saved.html",
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
        "blogs/partial/blogs.html",
        {
            "blogs":results,
            "query":query,
            "tab":"search",
        }
    )


class BlogHandlerView(View):
    def get(self, request):
        return BlogServiceV1.get_creation_form(request)
    
    def post(self, request):
        return BlogServiceV1.create_blog(request)
    
    def update(self, request):
        pass

    def delete(self, request):
        pass

    
    
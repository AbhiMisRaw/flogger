from django.shortcuts import render
from django.views import View
# from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q
from .models import Blog
from .blog_service import BlogServiceV1, BlogAPIService
# Create your views here.


class BlogHome(View):
    def get(self, request):
        return BlogServiceV1.get_homepage(request)


class SingleBlogSlugView(View):
    def get(self, request, slug: str):
        return BlogServiceV1.get_blog(request, slug)


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


class BlogGetApiViewV1(View):

    def get(self, request):
        return BlogAPIService.get_blogs(request)


@method_decorator(csrf_exempt, name='dispatch')
class BlogCreateAPIView(View):
    @csrf_exempt
    def post(self, request):
        return BlogAPIService.handle_blog_creation(request=request)

    def patch(request):
        pass

    def delete(reqeust):
        pass
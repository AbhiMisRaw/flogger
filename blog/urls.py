from django.urls import path
from .views import (
    search_blogs,
    BlogHandlerView,
    BlogHome,
    SingleBlogSlugView,
    BlogGetApiViewV1,
    BlogCreateAPIView
)

url_mvt_patterns = [
    path("homepage/", BlogHome.as_view(), name="home_page"),
    path("create/", BlogHandlerView.as_view(), name="create_blog"),
    path("search", search_blogs, name="search"),
    path("<str:slug>/", SingleBlogSlugView.as_view(), name="get_blog_by_slug" ),
    # path("saved/", saved_blogs, name="saved_blogs"),
    # path("my-blog/", my_blogs, name="my_blogs"),
    
    
]

url_api_patterns = [
    path("api/v1/blogs",BlogGetApiViewV1.as_view()),
    path("api/v1/blogs/create",BlogCreateAPIView.as_view()),
]

urlpatterns = tuple(url_mvt_patterns + url_api_patterns)

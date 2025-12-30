from django.urls import path
from .views import saved_blogs, my_blogs, search_blogs, BlogHandlerView, BlogHome

urlpatterns = (
    path("homepage/", BlogHome.as_view(), name="home_page"),
    path("saved/", saved_blogs, name="saved_blogs"),
    path("my-blog/", my_blogs, name="my_blogs"),
    path("search", search_blogs, name="search"),
    path("create/", BlogHandlerView.as_view(), name="create_blog"),
)

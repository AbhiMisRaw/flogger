from django.urls import path
from .views import home, saved_blogs, my_blogs, search_blogs, create_blog

urlpatterns = (
    path("homepage/", home, name="home_page"),
    path("saved/", saved_blogs, name="saved_blogs"),
    path("my-blog/", my_blogs, name="my_blogs"),
    path("search", search_blogs, name="search"),
    path("create/", create_blog, name="create_blog"),
)

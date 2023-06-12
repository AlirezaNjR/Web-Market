from django.urls import path
from .views import PostListView, PostCreateView, PostDetailView,\
    PostDeleteView, PostUpdateView, SearchView

app_name = 'Blog'

urlpatterns = [
    path("", PostListView.as_view(), name="List"),
    path("<int:pk>/Detail/", PostDetailView.as_view(), name="Detail"),

    path("Create/", PostCreateView.as_view(), name="Create"),
    path("<int:pk>/Update/", PostUpdateView.as_view(), name="Update"),
    path("<int:pk>/Delete/", PostDeleteView.as_view(), name="Delete"),

    path("Search/", SearchView.as_view(), name="Search")
]

from django.urls import path
from .views import DeleteCommentView


app_name = 'Comment'

urlpatterns = [
    path("Blog/<int:pk>/Delete/", DeleteCommentView.as_view(), name="Delete")
]

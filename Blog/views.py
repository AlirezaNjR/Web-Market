from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, ListView, TemplateView

from .models import PostModel
from .forms import PostCreateForm

from Comment.forms import BlogCommentForm
from Comment.models import BlogCommentModel
# Create your views here.


class PostListView(ListView):

    model = PostModel
    paginate_by = 10
    ordering = ['-created']
    context_object_name = 'Posts'
    template_name = 'Blog/blog.html'


class PostDetailView(DetailView):
    def post(self, request, *args, **kwargs):
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post = self.get_object()
            BlogCommentModel.objects.create(
                name=cd['name'],
                text=cd['text'],
                email=cd['email'],
                website=cd['website'],
                post=post,
            )
            return redirect('Blog:Detail', pk=post.pk)
        else :
            return HttpResponse('400')
    model = PostModel
    template_name = 'Blog/blog-Single.html'
    context_object_name = 'Post'


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = PostModel
    form_class = PostCreateForm
    template_name = 'Blog/create.html'
    login_url = 'Main:Home'
    success_url = reverse_lazy('Blog:List')

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = PostModel
    login_url = 'Main:Home'
    context_object_name = 'Post'
    template_name = 'Blog/delete.html'
    success_url = reverse_lazy('Blog:List')

    def post(self, request, *args, **kwargs):
        post = PostModel.objects.get(id=kwargs['pk'])
        if (request.user == post.author) or (request.user.is_superuser):
            if post.cover:
                post.delete_image()
            post.delete()
            return redirect('Blog:List')
        else:
            return HttpResponse('<h1 style="color:red;"> 403 </h1>')


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PostModel
    login_url = 'Main:Home'
    success_url = reverse_lazy('Blog:List')
    form_class = PostCreateForm
    template_name = 'Blog/create.html'

    def test_func(self) -> bool | None:
        obj = self.get_object()
        return (self.request.user == obj.author) or (self.request.user.is_superuser)

    def form_valid(self, form):
        obj = self.get_object()
        form.instance.author = obj.author
        return super().form_valid(form)


class SearchView(TemplateView):
    template_name = 'Blog/blog-search.html'

    def get(self, request, *args, **kwargs):
        key = request.GET.get('key')
        posts = PostModel.objects.filter(
            title__contains=key) | PostModel.objects.filter(description__contains=key)
        posts.order_by('-created')
        kwargs['Posts'] = posts
        kwargs['Key'] = key
        return super().get(request, *args, **kwargs)

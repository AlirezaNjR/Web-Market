from django.contrib import messages
from .models import BlogCommentModel
from django.shortcuts import redirect
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class DeleteCommentView(LoginRequiredMixin,DeleteView):
    def get(self, request, *args , **kwargs) :
        if request.user.is_superuser: # type: ignore
            BlogCommentModel.objects.get(pk=kwargs['pk']).delete()
            messages.success(request,'نظر  حذف شد')
            return redirect(request.GET.get('rd'))
        else:
            messages.error(request,'شما به این بخش دسترسی ندارید')
            return redirect('Blog:List')
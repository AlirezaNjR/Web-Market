from django.contrib import admin
from .models import PostModel
from martor.admin import AdminMartorWidget
from django.db.models import TextField
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        TextField: {'widget': AdminMartorWidget}
    }


admin.site.register(PostModel, PostAdmin)

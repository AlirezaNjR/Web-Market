from django.db import models
from Blog.models import PostModel
from django.utils.translation import gettext_lazy as _
# Create your models here.


class BlogCommentModel(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name=_("نام"),
        null=False,
        blank=False
    )
    email = models.EmailField(
        max_length=254,
        verbose_name=_("ایمیل"),
        null=False,
        blank=False
    )
    text = models.TextField(
        max_length=500,
        verbose_name=_("متن"),
        null=False,
        blank=False,
    )
    website = models.URLField(
        max_length=200,
        verbose_name=_("وبسایت"),
        null=True,
        blank=True
    )
    datetime = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_("زمان و تاریخ"),
        )

    post = models.ForeignKey(
        PostModel,
        on_delete=models.CASCADE,
        related_name='Comments',
        verbose_name=_("پست"),
    )

    class Meta:
        ordering = ('-datetime',)
        verbose_name = _('کامنت برای بلاگ')
        verbose_name_plural = _('کامنت های بلاگ')

    def __str__(self):
        return f'{self.name} برای پست {self.post.title}'

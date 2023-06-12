from django.db import models
from django.urls import reverse
from martor.models import MartorField
from Accounts.models import CustomUserModel
from os import remove as os_remove, path as os_path
from django.utils.translation import gettext_lazy as _
# Create your models here.


_IMAGES_LOCATION = lambda instanse, filename:  f'{instanse.author}/Blog/Cover/{filename}'


class PostModel(models.Model):
    title = models.CharField(
        max_length=150,
        verbose_name=_('عنوان'),
        null=False,
        blank=False,
    )
    description = MartorField(
        max_length=2000,
        verbose_name=_('متن'),
        null=False,
        blank=False,
    )
    cover = models.ImageField(
        upload_to=_IMAGES_LOCATION,
        verbose_name=_('عکس'),
        null=True,
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        CustomUserModel, on_delete=models.CASCADE, verbose_name=_('نویسنده'), )

    class Meta:
        ordering = ['-created']
        verbose_name = _('پست')
        verbose_name_plural = _('پست ها')

    def __str__(self) -> str:
        return f'{self.title}  توسط  {self.author}'

    def get_absolute_url(self):
        return reverse("Blog:Detail", kwargs={"pk": self.pk})

    def delete_image(self):
        try:
            os_path.isfile(self.cover.path)
            os_remove(self.cover.path)
        except:
            print(self.title, ' Remove Image Err')

from django.db import models
from os import remove as os_remove , path as os_path
from django.urls import reverse
from django.contrib.auth import get_user_model 
from django.utils.translation import gettext_lazy as _
# Create your models here.
_IMAGES_LOCATION = lambda instanse, filename : f'{instanse.uploader}/{filename}'


class CategoriesModel(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    
    class Meta:
        ordering = ['name']
        verbose_name = _('دسته اصلی')
        verbose_name_plural = _(' دسته بندی اصلی ')
    
    def __str__(self) -> str:
        return f'{self.name}'

class CategoryModel(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    higher_category = models.ForeignKey(
        CategoriesModel,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='H_C',
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = _('دسته ')
        verbose_name_plural = _(' دسته بندی  ')
            
    def __str__(self) -> str:
        return f'{self.name}'

class SizingModel(models.Model):
    size = models.CharField(max_length=50, null=False, blank=False,verbose_name=_(' سایز '))

    class Meta:
        ordering = ['-size']
        verbose_name = _(' سایز ')
        verbose_name_plural = _(' سایز بندی ')
    
    def __str__(self) -> str:
        return str(self.size)

class ColorsModel(models.Model):
    name = models.CharField(max_length=50,null=False,blank=False,verbose_name=_(' رنگ '))
    
    class Meta:
        ordering = ['name']
        verbose_name = _('رنگ')
        verbose_name_plural = _('رنگ ها')
    
    def __str__(self) -> str:
            return str(self.name)
        
class ProductModel(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False,verbose_name=_('نام محصول'))
    description = models.TextField(max_length=500, null=False, blank=False,verbose_name=_('توضیحات'))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='User',
        verbose_name=_('نویسنده')
    )
    price = models.BigIntegerField(null=False, blank=False,verbose_name=_('قیمت'))
    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='Category',
        verbose_name=_('دسته بندی')
    )
    in_stock = models.BooleanField(default=False, null=False, blank=False,verbose_name=_('موجود است ؟'))
    size = models.ManyToManyField(SizingModel, related_name='Size',verbose_name=_('سایز های موجود'))
    colors = models.ManyToManyField(ColorsModel, related_name='Colors',verbose_name=_('رنگهای موجود'))
    count = models.PositiveIntegerField(default=1,null=False,blank=False)

    class Meta:
        ordering = ['-updated']
        verbose_name = _('محصول')
        verbose_name_plural = _('محصولات')

    def get_absolute_url(self):
        return reverse("Product:Detail", kwargs={"pk": self.pk})

    def get_images(self):
        return self.Images.all() # type: ignore
    
    def get_product_banner(self):
        image = self.Images.first() # type: ignore
        return image
    
    
    def __str__(self) -> str:
        return f'{self.name} توسط {self.user} در دسته بندی {self.category}'

class MultipleImageModel(models.Model):

    uploader = models.ForeignKey(
        get_user_model(), 
        related_name='Uploader', 
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=_(' بارگزار ')
        )
    image = models.ImageField(
        upload_to=_IMAGES_LOCATION, 
        null=False, 
        blank=False,
        verbose_name=_('عکس ')
        )

    for_product = models.ForeignKey(ProductModel, on_delete=models.CASCADE,related_name='Images',verbose_name=_('برای محصول'))
    
    class Meta:
        verbose_name = _('عکس چندگانه')
        verbose_name_plural = _('عکس های چندگانه')

    def __str__(self) -> str:
        return f'{self.image.url}'
    
    def delete_img(self):
        try:
            os_path.isfile(self.image.path)
            os_remove(self.image.path) 
        except :
            print('Delete File ERR')  


from django.contrib import admin
from .models import ProductModel , MultipleImageModel , CategoriesModel , \
    CategoryModel , SizingModel ,ColorsModel 



admin.site.register(ColorsModel)
admin.site.register(SizingModel)
admin.site.register(ProductModel)
admin.site.register(CategoryModel)
admin.site.register(CategoriesModel)
admin.site.register(MultipleImageModel)
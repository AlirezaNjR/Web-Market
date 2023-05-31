from django.urls import path
from .views import product_create_view, product_detail_view, product_delete_view, product_edit_view, \
    categories_view, category_view,\
    delete_image_view

app_name = 'Product'

urlpatterns = [
    path('<int:pk>/Create/', product_create_view, name='Create'),
    path('<int:pk>/Edit/', product_edit_view, name='Edit'),
    path('<int:pk>/Detail/', product_detail_view, name='Detail'),
    path('<int:pk>/Delete/', product_delete_view, name='Delete'),

    #! Category
    path('Categories/', categories_view, name='Categories'),
    path('Categories/<int:pk>', category_view, name='Category'),

    #! Images
    path('Images/<int:pk>/Delete/', delete_image_view, name='Image_Delete'), #type: ignore
]

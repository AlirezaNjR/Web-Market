from django.urls import path, include
from .views import CreateCartItemApiView, CartItemDeleteView, DeleteProductImageView

app_name = 'Api'

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('Cart/Add/', CreateCartItemApiView.as_view(), name='Add_CartItem'),
    path('Cart/Delete/<int:pk>/', CartItemDeleteView.as_view(), name='Delete_CartItem'),

    #! Product Image Urls
    path('Product/Image/<int:pk>/Delete/', DeleteProductImageView.as_view(), name='Delete_ProductImage'),
]

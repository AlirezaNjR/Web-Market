from django.urls import path
from .views import delete_cart_item_view, add_to_cart_view, \
    order_checkout_step_1, order_checkout_step_2, order_checkout_step_3, order_checkout_step_4,\
    order_cancell_view , user_order_list_view, user_order_detail_view

app_name = "Cart_Order"

urlpatterns = [
    path('Cart/Add/', add_to_cart_view, name='Add_CartItem'),  # type: ignore
    path('Cart/Delete/', delete_cart_item_view, name='Delete_CartItem'),

    #! Checkout & Order Urls
    path('Order/Checkout/Step-1/', order_checkout_step_1, name='Order_Checkout_1'),
    path('Order/Checkout/Step-2/', order_checkout_step_2, name='Order_Checkout_2'),
    path('Order/Checkout/Step-3/<int:pk>/', order_checkout_step_3, name='Order_Checkout_3'),
    path('Order/Checkout/Step-4/<int:pk>/', order_checkout_step_4, name='Order_Checkout_4'),
    path("Order/Cancell/", order_cancell_view , name="Order_Cancell"),
   
    #! User Orders
    path('Order/User/<int:pk>/List/', user_order_list_view, name='User_Orders'),
    path('Order/User/<int:pk>/Detail/', user_order_detail_view, name='User_Order_Detail'),
]

from django.urls import path
from .views import user_register_view, login_view, logout_user , edit_user_view

app_name = 'Accounts'

urlpatterns = [
    path('Login/', login_view, name='Login'),  # type: ignore
    path('Logout/',logout_user,name='Logout'), # type: ignore
    path('Register/', user_register_view, name='Register'),  # type: ignore
    path('Edit/<int:pk>/',edit_user_view,name='Edit_User'),
]

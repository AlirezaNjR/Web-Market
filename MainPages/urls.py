from django.urls import path
from .views import home_view, about_us_view, contact_view, search_view

app_name = 'Main'

urlpatterns = [
    path('', home_view, name='Home'),
    path('Search/', search_view, name='Search'), # type: ignore
    path('About-Us/', about_us_view, name='AboutUs'),
    path('Contact/', contact_view, name='Contact'),
]

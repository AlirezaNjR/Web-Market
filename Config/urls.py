from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from Config.settings import MEDIA_ROOT, MEDIA_URL, DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('MainPages.urls')),
    path('Product/', include('Product.urls')),
    path('Accounts/', include('Accounts.urls')),
    path('', include('Cart_Order.urls')),
    path('Api/V1/', include('Api.urls')),
    path('martor/', include('martor.urls')),
    path('Blog/', include('Blog.urls'))
]

handler404 = 'MainPages.views.err_404_view'

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from Config.settings import MEDIA_ROOT, MEDIA_URL, DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    #! Main Pages
    path('', include('MainPages.urls')),
    #! Product App
    path('Product/', include('Product.urls')),
    #! Accounts
    path('Accounts/', include('Accounts.urls')),
    #! Cart Order
    path('', include('Cart_Order.urls')),
    #! Api
    path('Api/V1/', include('Api.urls')),
    #! martor
    path('martor/', include('martor.urls')),
    #! Blog
    path('Blog/', include('Blog.urls')),
    #! Comments
    path("Comments/", include('Comment.urls'))
]

handler404 = 'MainPages.views.err_404_view'

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

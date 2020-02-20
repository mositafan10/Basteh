from django.urls import path, include 
from django.contrib import admin



urlpatterns = [
    path('', include('account.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('advertise/', include('advertise.urls')),
    path('blog/', include('blog.urls')),
    path('chat/', include('chat.urls')),
]

admin.site.site_header = "My site" # why not work ?

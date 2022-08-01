from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('project/', include('project.urls')),
    path('admin/', admin.site.urls)
]

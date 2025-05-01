from django.contrib import admin
from django.urls import path

# This is a custom wrapper around the admin site URLs to ensure proper loading
# It simply re-exports the standard admin site URLs

urlpatterns = [
    path('', admin.site.urls),  # Keep the standard admin URLs
] 
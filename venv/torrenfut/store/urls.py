from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('store/', views.store, name='store'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


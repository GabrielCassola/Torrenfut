from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('store/', views.store, name='store'),
    path('store/produto/<str:time>/<str:estilo>/<str:temporada>', views.produto, name='produto'),
    re_path(r'^store/produto/(?P<time>[^/]+)/(?P<estilo>[^/]+)/(?P<temporada>.+)$', views.produto, name='produto'),
]


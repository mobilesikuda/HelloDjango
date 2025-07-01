from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('catalogs/', views.catalogs, name='catalogs'),
    path('catalogs/admin', views.UploadJson, name='catalogs'),
    path('catalogs/saveexcell', views.SaveExcell, name='catalogs'),
    path('catalogs/<int:id>', views.details, name='details'),
    path('catalogs/api', views.CatalogAPI.as_view(), name='article-api'),
]

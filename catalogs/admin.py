from django.contrib import admin
from .models import Catalog

class CatalogAdmin(admin.ModelAdmin):
  list_display = ("name", "title",)


# Register your models here.
admin.site.register(Catalog, CatalogAdmin)

